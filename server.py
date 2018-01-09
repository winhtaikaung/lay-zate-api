import os
import tornado.options
import tornado.web
from tornado.ioloop import IOLoop

from db.db_helper import DBHelper
from handlers.base_handler import BaseHandler
from routes.messenger_route import messenger_routes
from routes.user_route import user_routes


class MainHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.respond("Invalid Request", 404)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler)
        ]

        settings = {
            'debug': True
        }
        # This Method is to add all the routes from Route Package
        handlers.extend(user_routes)
        handlers.extend(messenger_routes)
        tornado.web.Application.__init__(self, handlers, settings)
        tornado.options.parse_command_line()


def main():
    DBHelper().gen_schema()
    app = Application()
    app.listen(os.environ["PORT"])
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
