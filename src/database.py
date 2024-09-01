from aiofile import async_open
from fastapi import Depends, HTTPException, status
from sqlalchemy import Date, String, Text, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, \
    async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


async def uri() -> str:
    async with async_open('.secret', encoding='utf-8') as file:
        password = await file.read()

    return f'postgresql+asyncpg://postgres:{password}@localhost:5432/postgres'


engine: AsyncEngine = None


async def init_engine() -> None:
    global engine

    try:
        engine = create_async_engine(await uri())

        async with engine.connect() as conn:
            await conn.execute(text('SELECT 1'))
    except OperationalError as err:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            'Database connection failed: ' + str(err),
        )
    except SQLAlchemyError as err:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(err))


async def init_db_once() -> None:
    if not init_db_once.done:
        await init_engine()
        await init_db()

        init_db_once.done = True


init_db_once.done = False


async def get_db(db_init=Depends(init_db_once)):
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )

    try:
        async with async_session() as session:
            yield session
    except OperationalError as err:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            'Database connection failed: ' + str(err),
        )


class Base(DeclarativeBase):
    ...


class ContactDatabaseModel(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20))
    birthday: Mapped[str] = mapped_column(Date())
    bio: Mapped[str] = mapped_column(Text)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as err:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'Database initialization failed: ' + str(err),
        )
