from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_delete_close_project,
    check_delete_investing_project,
    check_name_duplicate,
    check_none,
    check_update_close_project,
    check_update_full_amount_project
)
from app.crud.charity_project import charity_project_crud
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investing import investing_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    check_none(charity_project.name, 'name')
    check_none(charity_project.description, 'description')
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
        commit=True
    )

    session.add_all(
        investing_process(
            new_charity_project,
            await charity_project_crud.get_open_objects(Donation, session)
        )
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_update_close_project(project_id, session)
    await check_update_full_amount_project(
        project_id, obj_in.full_amount, session
    )
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_delete_close_project(
        project_id, session
    )
    await check_delete_investing_project(
        project_id, session
    )
    return await charity_project_crud.remove(
        charity_project, session
    )
