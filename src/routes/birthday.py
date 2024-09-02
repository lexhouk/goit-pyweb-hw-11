from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import Entity
from src.schemas import Responses


async def action(db: AsyncSession, days: int) -> Responses:
    query = select(Entity).where(Entity.birthday.isnot(None))
    result = await db.execute(query)

    if not (entities := result.scalars().all()):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    result = []
    TODAY = date.today()

    for entity in entities:
        real = entity.birthday.replace(year=TODAY.year)

        if real < TODAY:
            real = real.replace(year=TODAY.year + 1)

        if 0 <= (real - TODAY).days <= days:
            result.append(entity)

    return result
