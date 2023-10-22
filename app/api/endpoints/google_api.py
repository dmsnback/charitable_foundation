from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service

from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)


URL_GOOGLE_SHEETS = 'https://docs.google.com/spreadsheets/d/'


router = APIRouter()


@router.get(
    '/',
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""

    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet[0], wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet[0], projects, wrapper_services
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    return spreadsheet[1]
