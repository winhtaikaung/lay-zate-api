import sqlalchemy as sa
from sqlalchemy import String

from entity.base import gen_uuid, Base


class Arrival(Base):

    def __init__(self):
        self.id = str(gen_uuid())

    _base_airport = sa.Column(String(10), index=True)
    query_time = sa.Column(sa.SMALLINT())
    flight = sa.Column(String(10))
    carrier = sa.Column(String(50))
    origin = sa.Column(String(50))
    arrival = sa.Column(String(20))
    status = sa.Column(String(30))
