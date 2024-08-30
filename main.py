from asyncio import sleep

from fastapi import FastAPI

app = FastAPI()


@app.get('/api/healthchecker')
async def root() -> dict:
    await sleep(1)

    return {'message': 'Welcome to FastAPI!'}


@app.post('/api/contacts')
async def create_contact() -> dict:
    ...


@app.get('/api/contacts')
async def read_contacts() -> dict:
    ...


@app.get('/api/contacts/birthdays')
async def read_birthday_contacts() -> dict:
    ...


@app.get('/api/contacts/{contact_id}')
async def read_contact(contact_id: int) -> dict:
    await sleep(1)

    return {'contact': contact_id}


@app.put('/api/contacts/{contact_id}')
async def update_contact(contact_id: int) -> dict:
    await sleep(1)

    return {'contact': contact_id}


@app.delete('/api/contacts/{contact_id}')
async def delete_contact(contact_id: int) -> dict:
    await sleep(1)

    return {'contact': contact_id}
