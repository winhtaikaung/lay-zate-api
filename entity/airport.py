import sqlalchemy as sa
from sqlalchemy import String

from entity.base import gen_uuid, Base


class Airport(Base):

    def __init__(self):
        self.id = str(gen_uuid())

    airport_name = sa.Column(String(200))
    country = sa.Column(String(50))
    airport_code = sa.Column(String(5))
    lat = sa.Column(String(30))
    lon = sa.Column(String(30))
