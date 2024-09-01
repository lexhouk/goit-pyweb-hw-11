from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text
from uvicorn import run

from src.database import ContactDatabaseModel, get_db


app = FastAPI()


class ContactRequestModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    last_name: Optional[str] = Field(min_length=2, max_length=40)
    email: Optional[EmailStr] = Field(min_length=6, max_length=50)
    phone_number: str = Field(min_length=3, max_length=20)
    birthday: Optional[date] = None
    bio: Optional[str] = None


class ContactResponseModel(BaseModel):
    id: int = Field(default=1, ge=1)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    bio: str

    class Config:
        from_attributes = True


@app.get('/api/healthchecker')
async def root(db: AsyncSession = Depends(get_db)) -> dict:
    try:
        if not await db.execute(text('SELECT 1')):
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Database is not configured correctly',
            )

        return {'message': 'Welcome to FastAPI!'}
    except Exception as err:
        print(err)

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'Error connecting to the database',
        )


@app.post('/api/contacts', status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactRequestModel,
    db: AsyncSession = Depends(get_db)
) -> ContactResponseModel:
    contact = ContactDatabaseModel(
        **body.model_dump(exclude_unset=True),
    )

    db.add(contact)

    await db.commit()
    await db.refresh(contact)

    return contact


@app.get('/api/contacts')
async def read_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = Query(None, pattern=r'^[^@]+@[^\.]+\.\w+$'),
    db: AsyncSession = Depends(get_db)
) -> list[ContactResponseModel]:
    query = select(ContactDatabaseModel)

    if first_name:
        query.where(ContactDatabaseModel.first_name == first_name)

    if last_name:
        query.where(ContactDatabaseModel.last_name == last_name)

    if email:
        query.where(ContactDatabaseModel.email == email)

    result = await db.execute(query)

    if not (result := result.scalars().all()):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    return result


@app.get('/api/contacts/birthdays')
async def read_birthday_contacts() -> dict:
    ...


async def get_contact(
    db: AsyncSession,
    contact_id: int
) -> ContactResponseModel:
    query = select(ContactDatabaseModel).filter_by(id=contact_id)
    result = await db.execute(query)

    if not (contact := result.scalar_one_or_none()):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    return contact


@app.get('/api/contacts/{contact_id}')
async def read_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db)
) -> ContactResponseModel:
    return await get_contact(db, contact_id)


@app.put('/api/contacts/{contact_id}')
async def update_contact(
    body: ContactRequestModel,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db)
) -> ContactResponseModel:
    if (contact := await get_contact(db, contact_id)):
        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)

        await db.commit()
        await db.refresh(contact)

    return contact


@app.delete(
    '/api/contacts/{contact_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_contact(
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db)
) -> None:
    if (contact := await get_contact(db, contact_id)):
        await db.delete(contact)
        await db.commit()


if __name__ == '__main__':
    run('main:app', host='0.0.0.0', port=8000, reload=True)
