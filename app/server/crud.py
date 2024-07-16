import base64

from fastapi import HTTPException
from sqlalchemy import select

from app.server.models import User, Role
from app.server.routers.units import hash_password
from app.server.schemas import UserModel, UserSchema


# async def create_user(self, user: UserModel) -> UserModel:
#     async with self.session() as session:
#         user = User(username=user.user_name, hashed_password=user.hashed_password)
#         session.add(user)
#         await session.commit()
#
#
# async def get_all_users(self):
#     async with self.session() as session:
#         print(1)
#         query = await session.execute(select(User))
#         # print(query.scalars().all())
#         print(query)
#
#         return query.scalars().all()

async def check_unique_value(session, user: UserModel):
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
        result = await check_unique_value(session,user)
        password = await hash_password(user.password)
        password = base64.b64encode(password).decode('utf-8')
        new_user  = User(username=user.username, email=user.email, password=password)
        session.add(new_user)
        await session.commit()
        print(new_user.id)
        new_role = Role(key=new_user.id, role='admin')
        session.add(new_role)
        await session.commit()
        print("User registered:", user)
        return new_user





