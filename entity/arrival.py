import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT

from entity.base import Base


class Arrival(Base):
    _base_airport = sa.Column(String(10), index=True)
    _query_time = sa.Column(sa.SMALLINT(), index=True)
    flight = sa.Column(String(10), index=True, )
    carrier = sa.Column(String(50), index=True)
    origin = sa.Column(String(50))
    arrival = sa.Column(String(20))
    status = sa.Column(String(30))
    fs_url = sa.Column(LONGTEXT())
    fs_api = sa.Column(LONGTEXT())
