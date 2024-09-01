from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Entity
from src.schemas import Request, Response


async def action(db: AsyncSession, body: Request) -> Response:
    contact = Entity(**body.model_dump(exclude_unset=True))

    db.add(contact)

    await db.commit()
    await db.refresh(contact)

    return contact
