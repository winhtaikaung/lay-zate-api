import uuid as uuid

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())


def gen_uuid():
    return uuid.uuid4()


class BaseModel(object):
    query = DBSession.query_property()
    id = sa.Column(sa.String(255), primary_key=True, unique=True, default=str(gen_uuid()))

    @declared_attr
    def __tablename__(self):
        """
        This method will override the method of SqlAlchemy __tablename__ and generate the table names in lower
        :return:
        """
        return self.__name__.lower()


Base = declarative_base(cls=BaseModel)
