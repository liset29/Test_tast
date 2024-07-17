from sqlalchemy.ext.asyncio import AsyncSession

from app.server.crud import update_role_key
from app.server.db_helper import db_helper
from app.server import crud
from app.server.utils import validate_password, encode_jwt, decode_jwt, validate_auth_user, \
    get_curresnt_active_auth_user

from app.server.schemas import UserSchema, TokenInfo, UserModel, Registration, Registered
from fastapi import APIRouter, Depends, Form, HTTPException, status, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from app.server.utils_db import get_user

http_bearer = HTTPBearer()

auth_router = APIRouter(prefix="/user", tags=['USER'])


# async def validate_auth_user(
#         username: str = Form(),
#         password: str = Form(),
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                  detail='invalid username or password')
#
#     user = await get_user(username, session)
#     if not user:
#         raise unauthed_exc
#     valid_password = validate_password(
#         password=password, hashed_password=user.password, )
#     if not valid_password:
#         raise unauthed_exc
#     if not user.active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail='user inactive')
#     return user
#
#
# async def get_curresnt_token_payload(
#         credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
# ):
#     token = credentials.credentials
#     try:
#         payload = await decode_jwt(token=token)
#     except InvalidTokenError:
#
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail=f'invalid token error')
#     return payload
#
#
# async def get_curresnt_auth_user(
#         payload: dict = Depends(get_curresnt_token_payload),
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)
# ) -> UserSchema:
#     username: str | None = payload.get('sub')
#
#     user = await get_user(username, session)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Invalid token or user not found')
#
#     return user
#
#
# async def get_curresnt_active_auth_user(
#         user: UserSchema = Depends(get_curresnt_auth_user)
# ):
#     if user.active:
#         return user
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                         detail='user inactive')


@auth_router.post("/login/", response_model=TokenInfo,
                  description='Endpoint that issues jwt token',
                  response_description="Token",
                  status_code=status.HTTP_200_OK,
                  response_model_by_alias=False
                  )
async def auth_user(user: UserSchema = Depends(validate_auth_user),
                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    jwt_payload = {'sub': user.username,
                   'email': user.email}

    token = await encode_jwt(jwt_payload)
    await update_role_key(token, user.username, session)

    return TokenInfo(access_token=token, token_type='Bearer')


@auth_router.get('/users/me', description='Endpoint that shows the data of users who have passed authentication',
                 response_description="User",
                 response_model=UserModel,
                 status_code=status.HTTP_200_OK,
                 response_model_by_alias=False)
async def auth_user_check(
        user: UserSchema = Depends(get_curresnt_active_auth_user)
):
    user = UserModel(username=user.username, email=user.email)
    return user


@auth_router.post('/registration/',
                  description='Endpoint that create admin',
                  response_description="New user",
                  response_model=Registered,
                  status_code=status.HTTP_201_CREATED,
                  response_model_by_alias=False
                  )
async def registration(user: Registration = Body(),
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    print(1)
    result = await crud.registration(user=user, session=session)
    return result