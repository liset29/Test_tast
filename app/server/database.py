from app.server.models import Base
import config as con
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f'postgresql+asyncpg://{con.USER}:{con.PASSWORD}@{con.HOST}:5432/{con.DATABASE}'

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
