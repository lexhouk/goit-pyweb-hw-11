from sqlalchemy.ext.asyncio import AsyncSession

from .helper import get


async def action(db: AsyncSession, contact_id: int) -> None:
    if (contact := await get(db, contact_id)):
        await db.delete(contact)
        await db.commit()
