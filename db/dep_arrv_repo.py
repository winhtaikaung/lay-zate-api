from tornado.ioloop import IOLoop

from db.dao import Dao
from entity.base import DBSession


class DepRepository(Dao):

    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        self.db_session = DBSession
        pass


class ArrvRepository(Dao):
    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        self.db_session = DBSession
        pass
