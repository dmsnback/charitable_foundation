from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_new_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        """Поиск в БД одноименного проекта"""

        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )

        return db_project_id.scalars().first()

    async def get_charity_project_by_id(
            self,
            project_id: int,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        """Получения объекта по ID """

        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )

        return db_project.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        """Сортирует список со всеми закрытыми проектами."""

        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1
            ).order_by(CharityProject.close_date - CharityProject.create_date)
        )

        return db_project.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
