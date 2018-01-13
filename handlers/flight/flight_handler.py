import calendar
import datetime

import os
import requests
import tornado
from tornado import gen

from db.dep_arrv_repo import DepRepository, ArrvRepository
from db.raw_repo import CacheRepository
from entity.arrival import Arrival
from entity.departure import Departure
from handlers.base_handler import BaseHandler
from scraper.lay_zate_scrapper import LayZateScrapper


class FlightHandler(BaseHandler):

    @tornado.web.asynchronous
    @gen.engine
    def get(self, airport_code, arv_dep_type, query_time):
        d = datetime.datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        response = []
        api_result = [];
        limit = self.get_argument("limit", int(10), True)  # <--- get query_argement
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
        initial_cache = yield gen.Task(cache_repo.get_raw, airport_code, query_time, arv_dep_type,
                                       )
        if initial_cache is not None:
            if unixtime - initial_cache.updated_timestamp > 600:
                flight_requst = requests.post(base_url, data=params,
                                              headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'})
                raw_response = yield gen.Task(cache_repo.upsert_and_cache_raw, airport_code, query_time, arv_dep_type,
                                              flight_requst.content)

                if raw_response["response_html"] is not None:
                    response = yield gen.Task(LayZateScrapper.get_scrapped_result, self, raw_response["response_html"],
                                              airport_code, query_time)
                    if arv_dep_type is '0':
                        yield gen.Task(dep_repo.bulk_upsert_by_query_time_ap_code, response, Departure, query_time,
                                       airport_code)
                        api_result = yield gen.Task(dep_repo.get_flights_by_query_time, Departure, limit, page,
                                                    query_time,
                                                    airport_code)
                    else:
                        yield gen.Task(arrv_repo.bulk_upsert_by_query_time_ap_code, response, Arrival, query_time,
                                       airport_code)
                        api_result = yield gen.Task(dep_repo.get_flights_by_query_time, Arrival, limit, page,
                                                    query_time,
                                                    airport_code)

            else:
                if arv_dep_type is '0':
                    api_result = yield gen.Task(dep_repo.get_flights_by_query_time, Departure, limit, page, query_time,
                                                airport_code)
                else:
                    api_result = yield gen.Task(dep_repo.get_flights_by_query_time, Arrival, limit, page, query_time,
                                                airport_code)

        else:
            flight_requst = requests.post(base_url, data=params,
                                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'})
            raw_response = yield gen.Task(cache_repo.upsert_and_cache_raw, airport_code, query_time, arv_dep_type,
                                          flight_requst.content)
            if raw_response["response_html"] is not None:
                response = yield gen.Task(LayZateScrapper.get_scrapped_result, self, raw_response["response_html"],
                                          airport_code, query_time)

            if arv_dep_type is '0':
                yield gen.Task(dep_repo.bulk_upsert_by_query_time_ap_code, response, Departure, query_time,
                               airport_code)
                api_result = yield gen.Task(dep_repo.get_flights_by_query_time, Departure, limit, page, query_time,
                                            airport_code)
            else:
                yield gen.Task(arrv_repo.bulk_upsert_by_query_time_ap_code, response, Arrival, query_time, airport_code)
                api_result = yield gen.Task(dep_repo.get_flights_by_query_time, Arrival, limit, page, query_time,
                                            airport_code)

        if api_result is not None:
            self.respond(
                api_result["data"],
                api_result["meta_obj"],
                200)
        else:
            self.respond(
                response,
                {"airport_code": str(airport_code), "query_type": str(arv_dep_type), "query_time": str(query_time)},
                200)


class AirportCodeFlightHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self, airport_code):
        self.respond({"airport_code": str(airport_code)}, {}, 200)
