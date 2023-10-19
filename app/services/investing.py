from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.schemas.donation import DonationDB
from app.schemas.charity_project import CharityProjectDB


async def invest_in_project(
        donation: DonationDB,
        session: AsyncSession
):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        ).order_by('create_date')
    )

    projects = projects.scalars().all()

    for project in projects:
        investing_process(donation, project, session)

    await session.commit()
    await session.refresh(donation)


async def invest_from_donation(
        project: CharityProjectDB,
        session: AsyncSession
):
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        ).order_by('create_date')
    )

    donations = donations.scalars().all()

    for donation in donations:
        investing_process(donation, project, session)

    await session.commit()
    await session.refresh(project)


def investing_process(
    donation,
    project,
    session: AsyncSession
):
    free_money = donation.full_amount - donation.invested_amount
    need_money = project.full_amount - project.invested_amount

    if free_money < need_money:
        project.invested_amount += free_money
        donation.invested_amount = donation.full_amount
        donation.fully_invested = 1
        donation.close_date = datetime.now()

    elif free_money >= need_money:
        project.invested_amount = project.full_amount
        donation.invested_amount += need_money
        project.fully_invested = 1
        project.close_date = datetime.now()

        if free_money == need_money:
            donation.fully_invested = 1
            donation.close_date = datetime.now()

    session.add(project)
    session.add(donation)
