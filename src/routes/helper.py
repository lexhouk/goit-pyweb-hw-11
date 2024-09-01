from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Entity
from src.schemas import Response


async def get(db: AsyncSession, contact_id: int) -> Response:
    query = select(Entity).filter_by(id=contact_id)
    result = await db.execute(query)

    if not (contact := result.scalar_one_or_none()):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    return contact
