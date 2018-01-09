import sqlalchemy as sa

from entity.base import Base, gen_uuid


class User(Base):

    def __init__(self):
        self.id = str(gen_uuid())

    sender_id = sa.Column(sa.String(50))
    recipient_id = sa.Column(sa.String(50))
    is_zawgyi = sa.Column(sa.Boolean, default=True)
    _defined_airport = sa.Column(sa.String(50))

    def _get_val(self):
        return ({
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'is_zawgyi': self.is_zawgyi
        })
