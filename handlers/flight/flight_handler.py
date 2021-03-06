import calendar
import datetime
import os
import urllib

import tornado
import json
from pyquery import PyQuery as pq
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from db.dep_arrv_repo import DepRepository, ArrvRepository
from db.raw_repo import CacheRepository
from entity.arrival import Arrival
from entity.departure import Departure
from handlers.base_handler import BaseHandler
from middleware.paging_validator import base_query_string_validator
from scraper.lay_zate_scrapper import LayZateScrapper


def get_api_result(self, api_result):
    if api_result is not None:
        self.respond(
            api_result["data"],
            api_result["meta_obj"],
            200)
    else:
        self.write("APIResult",
                   200)


class FlightHandler(BaseHandler):

    async def extract_table(self, base_url, params):
        flight_requst = await AsyncHTTPClient().fetch(base_url, body=urllib.parse.urlencode(params), method="POST",
                                                      headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'})

        d = pq(flight_requst.body)
        table = d.find(".tableListingTable").html()
        return str(table).encode('utf-8')

    @base_query_string_validator
    async def get(self, airport_code, arv_dep_type, query_time):
        d = datetime.datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        response = []
        api_result = []

        limit = self.get_argument("limit", int(
            10), True)  # <--- get query_argement
        page = self.get_argument("page", int(1), True)
        params = {'language': 'English',
                  'startAction': 'AirportFlightStatus',
                  'imageColor': 'orange',
                  'airportQueryTimePeriod': str(query_time),
                  'airportQueryType': str(arv_dep_type)
                  }
        dep_repo = DepRepository()
        arrv_repo = ArrvRepository()
        cache_repo = CacheRepository()
        base_url = str(os.environ["FLIGHT_BASE_URL"]).format(airport_code)

        initial_cache = await cache_repo.get_raw(airport_code, query_time, arv_dep_type)
        http = AsyncHTTPClient()
        if initial_cache is not None:
            if unixtime - initial_cache.updated_timestamp > 1000:
                table = await self.extract_table(base_url, params)
                raw_response = await cache_repo.upsert_and_cache_raw(airport_code, query_time, arv_dep_type,
                                                                     table)

                if raw_response["response_html"] is not None:
                    response = await LayZateScrapper.get_scrapped_result(self, raw_response["response_html"],
                                                                         airport_code, query_time)
                    if arv_dep_type is '0':
                        dep_repo.bulk_upsert_by_query_time_ap_code(response, Departure, query_time,
                                                                   airport_code)
                        api_result = dep_repo.get_flights_by_query_time(Departure, limit, page,
                                                                        query_time,
                                                                        airport_code)
                        get_api_result(self, api_result)
                    else:
                        arrv_repo.bulk_upsert_by_query_time_ap_code(response, Arrival, query_time,
                                                                    airport_code)
                        api_result = dep_repo.get_flights_by_query_time(Arrival, limit, page,
                                                                        query_time,
                                                                        airport_code)
                        get_api_result(self, api_result)
            else:
                if arv_dep_type is '0':
                    api_result = dep_repo.get_flights_by_query_time(Departure, limit, page, query_time,
                                                                    airport_code)
                    get_api_result(self, api_result)
                else:
                    api_result = dep_repo.get_flights_by_query_time(Arrival, limit, page, query_time,
                                                                    airport_code)
                    get_api_result(self, api_result)

        else:
            table = await self.extract_table(base_url, params)
            raw_response = await cache_repo.upsert_and_cache_raw(airport_code, query_time, arv_dep_type,
                                                                 table)
            if raw_response["response_html"] is not None:
                response = await LayZateScrapper.get_scrapped_result(self, raw_response["response_html"],
                                                                     airport_code, query_time)

            if arv_dep_type is '0':
                dep_repo.bulk_upsert_by_query_time_ap_code(response, Departure, query_time,
                                                           airport_code)
                api_result = dep_repo.get_flights_by_query_time(Departure, limit, page, query_time,
                                                                airport_code)
                get_api_result(self, api_result)
            else:
                arrv_repo.bulk_upsert_by_query_time_ap_code(
                    response, Arrival, query_time, airport_code)
                api_result = dep_repo.get_flights_by_query_time(Arrival, limit, page, query_time,
                                                                airport_code)
                get_api_result(self, api_result)


class AirportCodeFlightHandler(BaseHandler):
    async def get(self, flight_code, flight_number):
        import datetime
        now = datetime.datetime.now()
        base_url = str(os.environ["TRACK_URL"]).format(
            flight_code, flight_number, str(now.year), str(now.month), str(now.day))
        try:
            flight_requst = await AsyncHTTPClient().fetch(base_url, method="GET",
                                                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'})

            self.respond(json.loads(
                flight_requst.body.decode('utf8'))["data"], 200)
        except Exception as e:
            self.respond(str(e), 500)
