import base64
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.server.models import User, Role
from app.server.utils import hash_password, encode_jwt
from app.server.schemas import UserUpdate, Registration, CreateUser, Registered
from app.server.utils_db import get_user


async def create_new_user(user: CreateUser, session):                                        #создаёт нового пользователя
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


async def get_all_users(session) -> List[dict]:                                                 #достаёт список всех пользователей из базы данных и возвращает список пользователйе
    async with session() as async_session:
        stmt = select(User.username, User.email, User.id).where(User.active == True)
        result = await async_session.execute(stmt)
        users = result.fetchall()
        return [{"user_id": user_id, "username": username, "email": email} for username, email, user_id in users]


async def update_user_information(user_id: int, user_update: UserUpdate, session: AsyncSession,  # обновляет переданную информацию о пользователе
                                  current_user) -> UserUpdate:

    if current_user.role.name == 'user' and (
            current_user.user_id != user_id or current_user.role.name == 'user' and user_update.role == 'admin'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access is denied')
    await check_unique_value(session, user_update)
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
        role = await session.execute(select(Role).where(Role.user_id == user_id))
        existing_role = role.scalars().first()
        if existing_role:
            existing_role.role = user_update.role

    await session.commit()
    return UserUpdate(
        username=user.username,
        email=user.email,
        active=user.active,
        role=user_update.role
    )


async def delete_some_user(user_id: int, session: AsyncSession) -> dict:                 # удаляет пользователя по user_id
    try:
        user = await get_user(user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User_id {user_id} not found")
        await session.delete(user)
        await session.commit()
        return {"detail": f"User '{user_id}' deleted successfully"}

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")


async def check_unique_value(session: AsyncSession, user: CreateUser | UserUpdate):                  # при создании или обновлении пользователя проверяет уникальность username и email
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


async def registration(user: Registration, session) -> Registered:
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
        new_user = Registered(id=new_user.id,username = new_user.username,email = new_user.email, active = new_user.active, role = new_role.role )
        return new_user


async def update_role_key(key: str, username: str, session) -> None:                                # обновляет ключ к роли  у пользователя при получении нового ключа
    user = await get_user(username, session)
    role_key = await session.execute(select(Role).where(Role.user_id == user.id))  # hello every body
    existing_role_key = role_key.scalars().first()
    existing_role_key.key = key
    await session.commit()