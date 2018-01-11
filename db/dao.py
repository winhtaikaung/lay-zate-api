from tornado.ioloop import IOLoop

from entity.base import DBSession


class Dao(object):

    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        self.db_session = DBSession
        pass

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
        call_back(result)

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
