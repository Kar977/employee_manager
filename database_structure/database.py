from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from urllib.parse import quote
from sqlalchemy import create_engine


USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB_NAME = "employee_manager_db"


SYNC_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


def init_database():
    sync_engine = create_engine(SYNC_DATABASE_URL)
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)


init_database()

sync_engine = create_engine(SYNC_DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL)


SesionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with SesionLocal() as session:
        yield session
