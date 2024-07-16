from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.server.crud import get_all_users, delete_some_user, update_user_information, create_new_user, check_role_user
from app.server.db_helper import db_helper
from app.server.schemas import UserUpdate, CreateUser

users_router = APIRouter(prefix="/users", tags=['USERS'])



@users_router.get("/list/",
                  description='Endpoint that show all users',
                  response_description="List all users",
                  response_model=List,
                  response_model_by_alias=False)
async def list_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    users = await get_all_users(session)
    print(users)
    return users


@users_router.delete("/{user_id}", description="Endpoint which removes user")
async def delete_user(user_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    delete_result = await delete_some_user(user_id, session)
    return delete_result


@users_router.put("/{user_name}",
                  description='Endpoint which updates user data',
                  response_description="Update a user",
                  response_model=UserUpdate,
                  response_model_by_alias=False,
                  )
async def update_user(user_id: int,
                      user: UserUpdate = Depends(),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    result_update = await update_user_information(user_id, user, session)
    return result_update


@users_router.post("/",
                   description='Endpoint that adds a new user',
                   response_description="New user",
                   # response_model=CreateUser,
                   status_code=status.HTTP_201_CREATED,
                   response_model_by_alias=False, )
async def create_user(user: CreateUser = Body(),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_user = await create_new_user(user, session)
    return new_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    check_result = await check_role_user(credentials.credentials, session)
    print(check_result)


@users_router.get("/protected-endpoint")
async def protected_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": f"Доступ разрешен для пользователя {current_user}"}
