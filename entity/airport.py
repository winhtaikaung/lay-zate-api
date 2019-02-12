import sqlalchemy as sa
from sqlalchemy import String

from entity.base import Base


class Airport(Base):
    airport_name = sa.Column(String(200))
    country = sa.Column(String(50))
    airport_code = sa.Column(String(5))
    lat = sa.Column(String(30))
    lon = sa.Column(String(30))
