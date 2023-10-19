from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_none(
        obj: str,
        session: AsyncSession,
) -> None:
    """Проверка на пустое поле"""

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Поле не может быть пустым'
        )


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверка на дубликат имени проекта"""

    project_id = await charity_project_crud.get_new_project_id_by_name(
        project_name, session
    )

    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка, что проект есть в базе"""

    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )

    if not charity_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )

    return charity_project


async def check_delete_investing_project(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """проверка, что в проекте нет инвестиций"""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )

    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',

        )

    return charity_project


async def check_delete_close_project(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """проверка, что закрытый проект нельзя удалить"""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )

    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',

        )

    return charity_project


async def check_update_close_project(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка, что проект не закрыт"""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )

    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )

    return charity_project


async def check_update_full_amount_project(
        project_id: int,
        full_amount: int,
        session: AsyncSession
):
    """Проверка корректности требуемой суммы"""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if full_amount:
        if full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='При редактировании проекта нельзя '
                       'устанавливать требуемую сумму меньше внесённой.'
            )

    return charity_project
