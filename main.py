from asyncio import sleep
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
    birthday: Optional[str] = Field(min_length=10, max_length=10)
    bio: Optional[str] = None


class ContactResponseModel(BaseModel):
    id: int = Field(default=1, ge=1)
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: str
    bio: str

    class Config:
        from_attributes = True


@app.get('/api/healthchecker')
async def root(db: AsyncSession = Depends(get_db)) -> dict:
    try:
        result = await db.execute(text('SELECT 1'))

        if result is None:
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


@app.post('/api/contacts')
async def create_contact(
    contact: ContactRequestModel,
    db: AsyncSession = Depends(get_db)
) -> ContactResponseModel:
    new_contact = ContactDatabaseModel(
        **contact.model_dump(exclude_unset=True),
    )

    db.add(new_contact)

    await db.commit()
    await db.refresh(new_contact)

    return new_contact


@app.get('/api/contacts')
async def read_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = Query(None, regex=r'^[^@]+@[^\.]+\.\w+$'),
    db: AsyncSession = Depends(get_db)
) -> list[ContactResponseModel]:
    query = select(ContactDatabaseModel)

    if first_name:
        query.where(ContactDatabaseModel.first_name == first_name)

    if last_name:
        query.where(ContactDatabaseModel.last_name == last_name)

    if email:
        query.where(ContactDatabaseModel.email == email)

    try:
        result = await db.execute(query)
    except Exception:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    return result.scalars().all()


@app.get('/api/contacts/birthdays')
async def read_birthday_contacts() -> dict:
    ...


@app.get('/api/contacts/{contact_id}')
async def read_contact(contact_id: int = Path(ge=1)) -> dict:
    await sleep(1)

    return {'contact': contact_id}


@app.put('/api/contacts/{contact_id}')
async def update_contact(
    contact: ContactRequestModel,
    contact_id: int = Path(ge=1)
) -> dict:
    await sleep(1)

    return {'contact': contact_id}


@app.delete('/api/contacts/{contact_id}')
async def delete_contact(contact_id: int = Path(ge=1)) -> dict:
    await sleep(1)

    return {'contact': contact_id}


if __name__ == '__main__':
    run('main:app', host='0.0.0.0', port=8000, reload=True)
