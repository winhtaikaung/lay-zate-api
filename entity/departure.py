import sqlalchemy as sa
from sqlalchemy import String

from entity.base import Base


class Departure(Base):
    _base_airport = sa.Column(String(10), index=True)
    _query_time = sa.Column(sa.SMALLINT(), index=True)
    flight = sa.Column(String(10), index=True)
    carrier = sa.Column(String(50), index=True)
    destination = sa.Column(String(50))
    departure = sa.Column(String(20))
    status = sa.Column(String(30))
