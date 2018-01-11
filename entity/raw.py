import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT

from entity.base import gen_uuid, Base


class Raw(Base):
    def __init__(self):
        self.id = str(gen_uuid())

    _base_airport = sa.Column(String(10), index=True)
    query_time = sa.Column(String(10))
    query_type = sa.Column(String(2))
    response = sa.Column(LONGTEXT())
    updated_timestamp = sa.Column(sa.BIGINT())
