from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.server.models import User


async def get_user(value: str | int, session: AsyncSession):
    if type(value) == str:
        stmt_username = select(User).where(User.username == value)
    else:
        stmt_username = select(User).where(User.id == value)
    result_username = await session.execute(stmt_username)
    user = result_username.scalars().first()
    return user
