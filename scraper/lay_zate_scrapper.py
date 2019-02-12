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
        fetch_header = pq(d.find(".tableListingTable").html()).find(".header")

        flight_list_html = pq(d.find(".tableListingTable").html()) \
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

        return col_dict

    async def get_scrapped_result(self, html, base_airport, query_time):
        return LayZateScrapper.scrap_response(self, html, base_airport, query_time)
