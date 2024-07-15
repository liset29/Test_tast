from datetime import timedelta, datetime

import bcrypt
import jwt
import config as con


def encode_jwt(payload: dict,
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


def decode_jwt(token: str,
               public_key: str = con.public_key,
               algorithm=con.algorithm):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str,
                      hashed_password: bytes) -> bool:
    print(password)
    print(hashed_password)
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
