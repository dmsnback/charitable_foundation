from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetUser
from app.services.investing import invest_in_project


router = APIRouter()


@router.post(
    '/',
    response_model=DonationGetUser,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):

    new_donation = await donation_crud.create_donation(
        donation, user, session
    )

    await invest_in_project(new_donation, session)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
) -> list[str]:

    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationGetUser],
)
async def grt_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> list[str]:

    return await donation_crud.get_user_donation(user, session)
