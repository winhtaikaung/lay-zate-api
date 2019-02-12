import os
from os.path import dirname, join

import tornado.options
import tornado.web
from dotenv import load_dotenv
from tornado.ioloop import IOLoop

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
load_dotenv(dotenv_path, verbose=True)

from db.db_helper import DBHelper
from handlers.base_handler import BaseHandler
from routes.flight_route import flight_routes


class MainHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.respond("Not Found", 404)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler)
        ]

        # This Method is to add all the routes from Route Package
        handlers.extend(flight_routes)

        tornado.web.Application.__init__(self, handlers, debug=True)
        tornado.options.parse_command_line()


def main():
    DBHelper().gen_schema()
    app = Application()
    app.listen(os.environ["PORT"])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
