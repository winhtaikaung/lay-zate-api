import calendar
import datetime

from sqlalchemy import text
from tornado.ioloop import IOLoop

from entity.base import DBSession
from entity.raw import Raw


class RawRepository(object):
    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        self.db_session = DBSession
        pass

    def get_raw(self, base_airport, query_time, query_type,
                callback=None):
        session = self.db_session
        result = None
        sql = "SELECT * FROM raw where raw._base_airport =:base_airport AND raw.query_time=:query_time AND query_type =:query_type  LIMIT 0,1"
        try:
            raw_list = session.query(Raw).from_statement(text(sql)).params(base_airport=base_airport,
                                                                           query_time=query_time,
                                                                           query_type=query_type).all()
            if len(raw_list) is not 0:
                result = raw_list[0]
            else:
                result = None
        except Exception as e:
            session.rollback()
            print(e)
            result = None
        session.close()
        callback(result)

    def upsert_and_cache_raw(self, base_airport, query_time, query_type, response,
                             callback=None):
        session = self.db_session
        result = {"response_html": ""}
        sql = "SELECT * FROM raw where raw._base_airport =:base_airport AND raw.query_time=:query_time AND query_type =:query_type  LIMIT 0,1"
        try:
            raw_list = session.query(Raw).from_statement(text(sql)).params(base_airport=base_airport,
                                                                           query_time=query_time,
                                                                           query_type=query_type).all()
            d = datetime.datetime.utcnow()
            unixtime = calendar.timegm(d.utctimetuple())
            if len(raw_list) is not 0:
                raw = raw_list[0]
                if raw.response != response.decode('ascii'):
                    raw.response = response
                    raw.updated_timestamp = unixtime
                    print("CACHED")
                    session.commit()
                    result = {"response_html": response}
                else:
                    raw.updated_timestamp = unixtime
                    session.commit()
                    result = {"response_html": raw.response}
            else:
                raw = Raw()
                raw._base_airport = base_airport
                raw.query_time = query_time
                raw.query_type = query_type
                raw.response = response
                raw.updated_timestamp = unixtime
                session.add(raw)
                session.commit()
                result = {"response_html": response}

        except Exception as e:
            session.rollback()
            result = e
        session.close()
        callback(result)
