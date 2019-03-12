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


def make_app(options):
    handlers = [
        (r"/?", MainHandler)
    ]

    # This Method is to add all the routes from Route Package
    handlers.extend(flight_routes)

    return tornado.web.Application(handlers, debug=options.debug)


def main():
    DBHelper().gen_schema()

    tornado.options.define("port", default=os.environ['PORT'] if 'PORT' in os.environ else 3000)
    # Specify whether the app should run in debug mode
    # Debug mode restarts the app automatically on file changes
    tornado.options.define("debug",
                           default=False if 'APP_ENV' in os.environ and os.environ[
                               'APP_ENV'] == 'production' else True)

    # Read settings/options from command line
    tornado.options.parse_command_line()

    # Access the settings defined
    options = tornado.options.options

    app = make_app(options)

    app.listen(os.environ["PORT"])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
