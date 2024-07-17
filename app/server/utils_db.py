from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.server.models import User, Role


async def get_user(value: str | int, session: AsyncSession) -> User:
    if type(value) == str:
        stmt_username = select(User).where(User.username == value)
    else:
        stmt_username = select(User).where(User.id == value)
    result_username = await session.execute(stmt_username)
    user = result_username.scalars().first()
    return user


async def check_role_user(key: str, session):
    role_key = await session.execute(select(Role).where(Role.key == key))
    existing_role_key = role_key.scalars().first()
    if not existing_role_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access is denied')

    return existing_role_key
