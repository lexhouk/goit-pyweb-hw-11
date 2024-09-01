from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Entity
from src.schemas import Response


async def action(
    db: AsyncSession,
    first_name: str = None,
    last_name: str = None,
    email: str = None
) -> list[Response]:
    query = select(Entity)

    if first_name:
        query.where(Entity.first_name == first_name)

    if last_name:
        query.where(Entity.last_name == last_name)

    if email:
        query.where(Entity.email == email)

    result = await db.execute(query)

    if not (result := result.scalars().all()):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    return result
