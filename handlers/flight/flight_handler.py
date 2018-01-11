import calendar
import datetime

import os
import requests
import tornado
from tornado import gen

from db.dep_arrv_repo import DepRepository, ArrvRepository
from db.raw_repo import RawRepository
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
        params = {'language': 'English',
                  'startAction': 'AirportFlightStatus',
                  'imageColor': 'orange',
                  'airportQueryTimePeriod': str(query_time),
                  'airportQueryType': str(arv_dep_type)
                  }
        dep_repo = DepRepository()
        arrv_repo = ArrvRepository()
        raw_repo = RawRepository()
        base_url = str(os.environ["FLIGHT_BASE_URL"]).format(airport_code)
        initial_raw = yield gen.Task(raw_repo.get_raw, airport_code, query_time, arv_dep_type,
                                     )
        if initial_raw is not None:
            if unixtime - initial_raw.updated_timestamp > 900:
                flight_requst = requests.post(base_url, data=params,
                                              headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'})
                raw_response = yield gen.Task(raw_repo.upsert_and_cache_raw, airport_code, query_time, arv_dep_type,
                                              flight_requst.content)

                if raw_response["response_html"] is not None:
                    response = yield gen.Task(LayZateScrapper.get_scrapped_result, self, raw_response["response_html"],
                                              airport_code, query_time)
                    if arv_dep_type is 0:
                        yield gen.Task(dep_repo.bulk_insert, response, Departure)
                    else:
                        yield gen.Task(arrv_repo.bulk_insert, response, Arrival)
            else:
                response = yield gen.Task(LayZateScrapper.get_scrapped_result, self, initial_raw.response, airport_code,
                                          query_time)
                if arv_dep_type is '0':
                    yield gen.Task(dep_repo.bulk_insert, response, Departure)
                else:
                    yield gen.Task(arrv_repo.bulk_insert, response, Arrival)
        else:
            flight_requst = requests.post(base_url, data=params,
                                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'})
            raw_response = yield gen.Task(raw_repo.upsert_and_cache_raw, airport_code, query_time, arv_dep_type,
                                          flight_requst.content)
            if raw_response["response_html"] is not None:
                response = yield gen.Task(LayZateScrapper.get_scrapped_result, self, raw_response["response_html"],
                                          airport_code, query_time)

            if arv_dep_type is '0':
                yield gen.Task(dep_repo.bulk_insert, response, Departure)
            else:
                yield gen.Task(arrv_repo.bulk_insert, response, Arrival)
        print(response)
        self.respond(
            {"flight_list": response},
            {"airport_code": str(airport_code), "query_type": str(arv_dep_type), "query_time": str(query_time)},
            200)

    def save_to_db(self, arv_dep_type, response, dep_repo, arrv_repo):
        if arv_dep_type is '0':
            yield gen.Task(dep_repo.bulk_insert, response, Departure)
        else:
            yield gen.Task(arrv_repo.bulk_insert, response, Arrival)


class AirportCodeFlightHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self, airport_code):
        self.respond({"airport_code": str(airport_code)}, {}, 200)
