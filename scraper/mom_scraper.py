from pyquery import PyQuery as pq
from tornado.ioloop import IOLoop

from const.messages import MSG_RECORD_NOT_FOUND, MSG_INTERNAL_SERVER_ERROR, MSG_RECORD_EXISTS, MSG_GOOD_BYE, \
    MSG_SERVICE_UNAVAILABLE
from utils import to_snake_case


class MOMScrapper(object):
    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        pass

    def scrap_response(self, html):
        dict_response = {"data": {}, "meta": ""}
        dict_meta = {}
        d = pq(html)
        title_html = pq(d.find('title').html())

        title_text = title_html.text()
        if "Not Available" in title_text:
            """
            TODO if Not available give empty dictionary 
            """
            dict_meta = {"code": 408,
                         "message": MSG_SERVICE_UNAVAILABLE}
            dict_response["meta"] = dict_meta
        elif "PEPOLENQM009" in title_text:
            """
            TODO if it exists Continue scraping 
            """
            dict_data = {}
            form_html = pq(d.find('form[name="enquiryForm"]').html())
            result_html = pq(form_html.find('.outerBox > table > tr'))

            result_html.each(lambda e, tb_row:
                             dict_data.update(
                                 {to_snake_case(
                                     pq(tb_row).text().split(":")[0].strip().replace(" ", "_")).replace("__",
                                                                                                        "_").replace(
                                     ".", ""):
                                      pq(tb_row).text().split(":")[
                                          1].strip()})
                             )
            dict_meta = {
                "code": 200,
                "message": str(MSG_RECORD_EXISTS).format(dict_data["name"], dict_data["application_no"],
                                                         dict_data["date_of_application"], dict_data["pass_type"],
                                                         dict_data["status"], MSG_GOOD_BYE)
            };
            dict_response["meta"] = dict_meta
            dict_response["data"] = dict_data
        elif "PEPOLENQM007" in title_text:
            dict_meta = {
                "code": 403,
                "message": MSG_RECORD_NOT_FOUND
            }
            dict_response["meta"] = dict_meta
        else:
            dict_meta = {
                "code": 503,
                "message": MSG_INTERNAL_SERVER_ERROR
            };
            dict_response["meta"] = dict_meta
        return dict_response

    def get_scrapped_result(self, html, callback=None):

        return callback(MOMScrapper.scrap_response(self, html))
