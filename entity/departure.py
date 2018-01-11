import sqlalchemy as sa
from sqlalchemy import String

from entity.base import gen_uuid, Base


class Departure(Base):
    def __init__(self):
        self.id = str(gen_uuid())

    _base_airport = sa.Column(String(10), index=True)
    query_time = sa.Column(sa.SMALLINT())
    flight = sa.Column(String(10))
    carrier = sa.Column(String(50))
    destination = sa.Column(String(50))
    departure = sa.Column(String(20))
    status = sa.Column(String(30))
