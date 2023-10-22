from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import PreBaseChairityAndDonaton


class Donation(PreBaseChairityAndDonaton):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
