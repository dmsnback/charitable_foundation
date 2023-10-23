from copy import deepcopy
from datetime import datetime
from typing import List, Any

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject


FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEET_BODY = {
    'properties': {
        'title': 'Отчет от',
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': ROW_COUNT,
                    'columnCount': COLUMN_COUNT
                }
            }
        }
    ]
}
TABLE_VALUES = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(
    wrapper_services: Aiogoogle
) -> tuple[Any, Any]:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = f'Отчет от {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_value = deepcopy(TABLE_VALUES)
    table_value[0].append(now_date_time)

    table_values = [
        *table_value,
        *[list(map(str,
                   [project.name,
                    project.close_date - project.create_date,
                    project.description])) for project in projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    row_count = len(table_values)
    column_count = max(map(len, table_value))
    if row_count > ROW_COUNT or column_count > COLUMN_COUNT:
        raise ValueError(
            f'Таблица состоит из {ROW_COUNT} строк и {COLUMN_COUNT} столбцов.'
            f'Вы передаете данные на {row_count} строк'
            f' и {column_count} столбцов'
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row_count}C{column_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
