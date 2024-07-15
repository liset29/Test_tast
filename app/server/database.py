import asyncio

from sqlalchemy import create_engine

from app.server.models import Base

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'liset29'
DATABASE = 'test_task'
PORT = 5432
DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

