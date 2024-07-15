from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'liset29'
DATABASE = 'test_task'
PORT = 5432
DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}'
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session