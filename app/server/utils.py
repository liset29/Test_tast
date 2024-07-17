from datetime import timedelta, datetime

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

import config as con

from app.server.db_helper import db_helper
from app.server.utils_db import check_role_user

http_bearer = HTTPBearer()
async def encode_jwt(payload: dict,
                     private_key: str = con.private_key,
                     algorithm: str = con.algorithm,
                     expire_minutes: int = con.access_token_expire,
                     expire_timedelta: timedelta | None = None):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
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
                     algorithm=con.algorithm):
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
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    check_result = await check_role_user(credentials.credentials, session)
    return check_result
