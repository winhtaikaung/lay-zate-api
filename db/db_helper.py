import os
from sqlalchemy import create_engine

from entity.base import Base as model_base
from entity.base import DBSession

url = os.environ["DB_URL_FORMAT"]
url = url.format(os.environ["DB_USER_NAME"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_PORT"],
                 os.environ["DB_NAME"])

# db_engine = create_engine(options.db_connection_str) for sqlite
db_engine = create_engine(url)


class DBHelper:
    def __init__(self):
        DBSession.configure(bind=db_engine)
        pass

    def gen_schema(self):
        model_base.metadata.create_all(db_engine)
