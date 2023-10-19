from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):

    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):

    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationGetUser(DonationCreate):

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationGetUser):

    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
