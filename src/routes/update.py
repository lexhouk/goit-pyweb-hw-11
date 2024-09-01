from sqlalchemy.ext.asyncio import AsyncSession

from .helper import get
from src.schemas import Request, Response


async def action(
    db: AsyncSession,
    body: Request,
    contact_id: int
) -> Response:
    if (contact := await get(db, contact_id)):
        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)

        await db.commit()
        await db.refresh(contact)

    return contact
