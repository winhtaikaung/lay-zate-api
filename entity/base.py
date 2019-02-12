import math
import time

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())


def gen_uuid():
    import uuid
    return str(uuid.uuid4())


def gen_cursor():
    return math.ceil(time.time())


class BaseModel(object):
    id = sa.Column(sa.String(255), primary_key=True, unique=True, default=gen_uuid)
    updated_timestamp = sa.Column(sa.BIGINT(), index=True, default=gen_cursor)
    created_timestamp = sa.Column(sa.BIGINT(), index=True, default=gen_cursor)

    @declared_attr
    def __tablename__(self):
        """
        This method will override the method of SqlAlchemy __tablename__ and generate the table names in lower
        :return:
        """
        return self.__name__.lower()


Base = declarative_base(cls=BaseModel)
