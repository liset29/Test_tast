import bcrypt
import jwt
import config as con
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.server.schemas import UserSchema
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from app.server.utils_db import get_user
from app.server.db_helper import db_helper
from app.server.utils_db import check_role_user

http_bearer = HTTPBearer()


async def encode_jwt(payload: dict,
                     private_key: str = con.private_key,
                     algorithm: str = con.algorithm,
                     expire_minutes: int = con.access_token_expire,
                     expire_timedelta: timedelta | None = None):  # функция для кодирования jwt tokena
    to_encode = payload.copy()
    now = datetime.utcnow()
    print(algorithm)
    print(type(expire_minutes))
    print(expire_timedelta)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=int(expire_minutes))
    to_encode.update(
        exp=expire,
        iat=now)
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


async def decode_jwt(token: str,
                     public_key: str = con.public_key,
                     algorithm=con.algorithm):  # функция для декодирования по токену, публитчному ключу и алгоритму
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


async def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)  # проверка правильности пароля


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)): # функция для получения роли пользователя
    check_result = await check_role_user(credentials.credentials, session)
    return check_result


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='invalid username or password')

    user = await get_user(username, session)
    if not user:
        raise unauthed_exc
    valid_password = validate_password(
        password=password, hashed_password=user.password, )
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