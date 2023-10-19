from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def create_donation(
            self,
            obj_in,
            user: User,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_user_donation(
            self,
            user: User,
            session: AsyncSession
    ) -> list[Donation]:

        user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )

        return user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
