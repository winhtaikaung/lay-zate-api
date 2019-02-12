import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT

from entity.base import Base


class Raw(Base):
    _base_airport = sa.Column(String(10), index=True)
    query_time = sa.Column(String(10))
    query_type = sa.Column(String(2))
    response = sa.Column(LONGTEXT())
