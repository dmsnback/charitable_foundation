from datetime import datetime
from typing import List

from app.core.db import PreBaseChairityAndDonaton


def investing_process(
    target: PreBaseChairityAndDonaton,
    sources: List[PreBaseChairityAndDonaton]
) -> List[PreBaseChairityAndDonaton]:
    objects = []
    for source in sources:
        free_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for new_source in target, source:
            new_source.invested_amount += free_amount
            if new_source.full_amount == new_source.invested_amount:
                new_source.fully_invested = 1
                new_source.close_date = datetime.now()
        objects.append(source)
    return objects
