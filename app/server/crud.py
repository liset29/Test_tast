import base64
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.server.models import User, Role
from app.server.utils import hash_password, encode_jwt
from app.server.schemas import UserModel, UserUpdate, CreateUser
from app.server.utils_db import get_user


async def create_new_user(user: CreateUser, session):
    async with session() as session:
        await check_unique_value(session, user)
        password = await hash_password(user.password)
        password = base64.b64encode(password).decode('utf-8')
        new_user = User(username=user.username, email=user.email, password=password)
        session.add(new_user)
        await session.commit()
        jwt_payload = {'sub': user.username,
                       'email': user.email}

        token = await encode_jwt(jwt_payload)
        new_role = Role(key=token, role=user.role, user_id=new_user.id)
        session.add(new_role)

        await session.commit()
        new_user = UserUpdate(username=new_user.username, email=new_user.email, role=user.role)
        return new_user


async def get_all_users(session) -> List[dict]:
    async with session() as async_session:
        stmt = select(User.username, User.email).where(User.active == True)
        result = await async_session.execute(stmt)
        users = result.fetchall()
        return [{"username": username, "email": email} for username, email in users]


async def update_user_information(user_id: int, user_update: UserUpdate, session: AsyncSession):
    user = await get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if value is None or value in ('admin', 'user'):
            continue
        setattr(user, key, value)
    await session.commit()

    user = await get_user(user_id, session)
    if user_update.role:
        role = await session.execute(select(Role).where(Role.key == user_id))
        existing_role = role.scalars().first()
        if existing_role:
            existing_role.role = user_update.role
        else:
            new_role = Role(key=user_id, role=user_update.role)
            session.add(new_role)
    await session.commit()
    return UserUpdate(
        username=user.username,
        email=user.email,
        active=user.active,
        role=user_update.role
    )


async def delete_some_user(user_id: int, session: AsyncSession) -> dict:
    try:
        user = await get_user(user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User_id {user_id} not found")
        await session.delete(user)
        await session.commit()
        return {"detail": f"User '{user_id}' deleted successfully"}

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")


async def check_unique_value(session: AsyncSession, user: UserModel):
    stmt_username = select(User).where(User.username == user.username)
    result_username = await session.execute(stmt_username)
    existing_user_username = result_username.scalar_one_or_none()
    if existing_user_username:
        raise HTTPException(status_code=400, detail="A user with this username already registered")

    stmt_email = select(User).where(User.email == user.email)
    result_email = await session.execute(stmt_email)
    existing_user_email = result_email.scalar_one_or_none()
    if existing_user_email:
        raise HTTPException(status_code=400, detail="A user with this email already registered")

    return True


async def registration(user: UserModel, session) -> User:
    async with session() as session:
        await check_unique_value(session, user)
        password = await hash_password(user.password)
        password = base64.b64encode(password).decode('utf-8')
        new_user = User(username=user.username, email=user.email, password=password)
        session.add(new_user)
        await session.commit()
        jwt_payload = {'sub': user.username,
                       'email': user.email}

        token = await encode_jwt(jwt_payload)
        new_role = Role(key=token, role='admin', user_id=new_user.id)
        session.add(new_role)
        await session.commit()
        return new_user


async def update_role_key(key: str, username: str, session) -> None:
    user = await get_user(username, session)
    role_key = await session.execute(select(Role).where(Role.user_id == user.id)) #hello every body
    existing_role_key = role_key.scalars().first()
    existing_role_key.key = key
    await session.commit()

# async def check_role_user(key:str,session)->bool:
#     print(key)
#     role_key = await session.execute(select(Role).where(Role.key == key))
#     existing_role_key = role_key.scalars().first()
#
#     role = existing_role_key.role.name
#
#     if role == 'user':
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail=f'invalid token error')



