from sqlalchemy import Column, String, Text

from app.core.db import PreBaseChairityAndDonaton


class CharityProject(PreBaseChairityAndDonaton):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
