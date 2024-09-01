from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .create import action as create
from .delete import action as delete
from .helper import get
from .read_birthday import action as read_birthday
from .read_one import action as read_one
from .update import action as update
from src.database import get_db
from src.schemas import Request, Response


router = APIRouter(prefix='/contacts', tags=['Contacts'])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: Request,
    db: AsyncSession = Depends(get_db)
) -> Response:
    return await create(db, body)


@router.get('/')
async def read_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = Query(None, pattern=r'^[^@]+@[^\.]+\.\w+$'),
    db: AsyncSession = Depends(get_db)
) -> list[Response]:
    return await read_one(db, first_name, last_name, email)


@router.get('/birthdays')
async def read_birthday_contacts() -> dict:
    return await read_birthday()


@router.get('/{contact_id}')
async def read_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db)
) -> Response:
    return await get(db, contact_id)


@router.put('/{contact_id}')
async def update_contact(
    body: Request,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db)
) -> Response:
    return await update(db, body, contact_id)


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db)
) -> None:
    await delete(db, contact_id)
