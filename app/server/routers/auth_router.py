from sqlalchemy.ext.asyncio import AsyncSession

from app.server.crud import add_user_role
from app.server.db_helper import db_helper
from app.server import crud
from app.server.utils import validate_password, encode_jwt, decode_jwt
from app.server.schemas import UserSchema, TokenInfo, UserModel
from fastapi import APIRouter, Depends, Form, HTTPException, status, Body, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from app.server.utils_db import get_user

http_bearer = HTTPBearer()

auth_router = APIRouter(prefix="/jwt", tags=['JWT'])

async def registration(user: UserModel = Body(),
                       session: AsyncSession = Depends(db_helper.scoped_session_dependency, )):
    print('всё заебись')
    result = await crud.registration(user=user, session=session)
    return result
async def validate_auth_user(
        # username: str = Form(),
        # password: str = Form(),
        user: UserModel,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='invalid username or password')


    new_user = await registration(user)
    # user = await get_user(user, session)

    if not user:
        raise unauthed_exc
    valid_password = validate_password(
        password=user.password, hashed_password=user.password, )
    if not valid_password:
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive')
    return user




async def get_curresnt_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):

    token = credentials.credentials
    try:
        payload = await decode_jwt(token=token)

    except InvalidTokenError:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'invalid token error')

    return payload


async def get_curresnt_auth_user(
        payload: dict = Depends(get_curresnt_token_payload),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> UserSchema:
    username: str | None = payload.get('sub')

    user = await get_user(username, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token or user not found')

    return user


async def get_curresnt_active_auth_user(
        user: UserSchema = Depends(get_curresnt_auth_user)
):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='user inactive')



@auth_router.post("/login/", response_model=TokenInfo)
def auth_user(user: UserModel = Depends(validate_auth_user)):
    jwt_payload = {'sub': user.username,
                   'email': user.email}
    token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type='Bearer')

@auth_router.get('/users/me')
async def auth_user_check(
        user: UserSchema = Depends(get_curresnt_active_auth_user)
):
    print(1)
    return {'username': user.username,
            'email': user.email}

# @auth_router.post('/registration/')
# async def registration(user: UserModel = Body(), session: AsyncSession = Depends(db_helper.scoped_session_dependency,)):
#     result = await crud.registration(user=user, session=session)
#     return result
