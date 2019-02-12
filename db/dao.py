import time

from sqlalchemy import and_
from tornado.ioloop import IOLoop

from db.db_helper import serialize_alchemy, generate_meta, gen_offset_from_page
from entity.base import DBSession


class Dao(object):

    def __init__(self, io_loop=None):
        self.db_session = DBSession
        pass

    async def get_flights_by_query_time(self, model={}, limit=10, page_number=0, query_time=None, airport_code=None,
                                        callback=None):
        session = self.db_session
        result = {}
        meta_obj = {}

        try:
            query = session.query(model) \
                .filter(and_(model._query_time == query_time,
                             (model._base_airport == airport_code))).limit(limit).offset(
                gen_offset_from_page(page_number,
                                     limit)
            ).all()
            all_query = session.query(model) \
                .filter(and_(model._query_time == query_time,
                             (model._base_airport == airport_code))).all()
            db_result = serialize_alchemy(query)
            meta_obj = generate_meta("flight", int(limit), int(page_number), len(all_query))
            result.update({"data": db_result, "meta_obj": meta_obj})

        except Exception as e:
            print(e)
            result = None
        return result

    def create(self, model={}, call_back=None):
        """
                Create a user in DB by passing user_orm
                :param word_model:
                :param callback:
                :return:
                """
        session = self.db_session
        result = True
        try:
            session.add(model)
            session.commit()
        except Exception as e:
            session.rollback()
            result = e
        session.close()
        IOLoop.instance().add_timeout(time.time() + 0.05, lambda:
        call_back(result))

    def bulk_insert(self, object_list=[], model={}, callback=None):
        session = self.db_session
        obj_list = object_list
        result = None
        try:
            session.bulk_insert_mappings(model, obj_list)
            session.commit()
            result = True
        except Exception as e:
            session.rollback()
            print(e)
        session.close()
        callback(result)

    async def bulk_upsert_by_query_time_ap_code(self, object_list=[], model={}, query_time=None, airport_code=None,
                                                callback=None):
        session = self.db_session
        obj_list = object_list
        result = None
        try:
            db_result = session.query(model).filter(and_(model._query_time == query_time,
                                                         (model._base_airport == airport_code))).all()
            if len(db_result) is not 0:
                session.query(model).filter(and_(model._query_time == query_time,
                                                 (model._base_airport == airport_code))).delete()
                session.commit()
                session.bulk_insert_mappings(model, obj_list)
                session.commit()
                result = True
            else:
                session.bulk_insert_mappings(model, obj_list)
                session.commit()
                result = True
        except Exception as e:
            session.rollback()
            print(e)
            result = None
        session.close()
        return result
