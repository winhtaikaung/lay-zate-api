from pyquery import PyQuery as pq
from tornado.ioloop import IOLoop

from utils import to_snake_case


class LayZateScrapper(object):
    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        pass

    def scrap_response(self, html):
        flight_list = []
        dict_meta = {}
        d = pq(html)
        fetch_header = pq(d.find(".tableListingTable").html()).find(".header")

        flight_list_html = pq(d.find(".tableListingTable").html()) \
            .remove(".header") \
            .find('tr')
        flight_list_html.each(lambda e, fl_row:
                              flight_list.append(
                                  LayZateScrapper.scrap_row(self, fl_row, pq(fetch_header).text().split(" ")))
                              )
        del flight_list[0]
        return flight_list

    def scrap_row(self, row, key_val):
        col_dict = {}
        pq(row).find("td").each(lambda i, td:
                                col_dict.update({
                                    to_snake_case(key_val[i]): pq(td).text().replace("*", "").replace("^", "").replace(
                                        "(", "").replace(")", "")
                                })
                                )

        return col_dict

    def get_scrapped_result(self, html, callback=None):
        return callback(LayZateScrapper.scrap_response(self, html))
