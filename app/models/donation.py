from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models import PreBaseChairityAndDonaton


class Donation(PreBaseChairityAndDonaton):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пожертвование принято от {self.user_id}\n'
            f'Комментарий: {self.comment}\n'
            f'{super().__repr__()}'
        )
