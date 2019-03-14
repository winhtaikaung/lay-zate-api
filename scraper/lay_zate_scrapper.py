import re
import time

from pyquery import PyQuery as pq
from tornado.ioloop import IOLoop

from entity.base import gen_uuid
from utils import to_snake_case


class LayZateScrapper(object):
    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance().add_timeout(time.time() + 1)
        pass

    def scrap_response(self, html, base_airport, query_time):
        flight_list = []
        dict_meta = {
            "_base_airport": base_airport,
            "query_time": query_time
        }
        d = pq(html)
        fetch_header = d.find(".header")

        flight_list_html = pq(d.html()) \
            .remove(".header") \
            .find('tr')
        flight_list_html.each(lambda e, fl_row:
                              flight_list.append(
                                  LayZateScrapper.scrap_row(self, fl_row, pq(fetch_header).text().split(" "),
                                                            base_airport, query_time)
                              )
                              )
        if len(flight_list) is not 0:
            del flight_list[0]
        return flight_list

    def scrap_row(self, row, key_val, base_airport, query_time):

        col_dict = {}
        pq(row).find("td").each(lambda i, td:
                                col_dict.update({
                                    to_snake_case(key_val[i]): pq(td).text().replace("*", "").replace("^", "").replace(
                                        "(", "").replace(")", ""),
                                    "_base_airport": base_airport,
                                    "_query_time": query_time,
                                    "id": str(gen_uuid())
                                })
                                )
        if bool(col_dict) is True:
            flight_number = col_dict["flight"].replace(" ", "")
            col_dict["flight"] = flight_number
            number = re.split('(?<![A-Z0-9])[A-Z0-9]{2}', flight_number)
            import datetime
            now = datetime.datetime.now()

            col_dict["fs_url"] = "https://www.flightstats.com/v2/flight-tracker/{0}/{1}/{2}/{3}/{4}".format(
                flight_number[0:2],
                number[1], str(now.year), str(now.month), str(now.day))

            col_dict["fs_api"] = "https://www.flightstats.com/v2/api-next/flight-tracker/{0}/{1}/{2}/{3}/{4}".format(
                flight_number[0:2],
                number[1], str(now.year), str(now.month), str(now.day))
            col_dict["track_url"] = "{0}://{1}/api/v1/track/{2}/{3}".format(
                self.request.protocol, self.request.host, flight_number[0:2],
                number[1])
            return col_dict

    async def get_scrapped_result(self, html, base_airport, query_time):
        return LayZateScrapper.scrap_response(self, html, base_airport, query_time)
