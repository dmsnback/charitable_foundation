from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class PreBaseChairityAndDonaton(Base):

    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    def __repr__(self):
        return(
            'Всего инвестировано: '
            f'{self.invested_amount} из {self.full_amount}.'
        )
