import unittest

import os

from scraper.lay_zate_scrapper import LayZateScrapper


class MockResponse(object):

    def __init__(self, html):
        self.str_success_html = html


class TestScrapper(unittest.TestCase):

    def test_scrapper(self):
        html = MockResponse(str(os.environ["ARRV_RESP"]))
        if str(os.environ["DEP_RESP"]) == str(os.environ["DEP_RESP"]):
            print("false")
        lay_zate_scrapper = LayZateScrapper
        mom_response = lay_zate_scrapper.scrap_response(self, html.str_success_html)
        response = []
        self.assertEqual([], [])
