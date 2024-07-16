from sqlalchemy.ext.asyncio import AsyncSession

from app.server.db_helper import db_helper
from app.server import crud
from app.server.routers.units import hash_password, validate_password, encode_jwt, decode_jwt
from app.server.schemas import UserSchema, TokenInfo, UserModel
from fastapi import APIRouter, Depends, Form, HTTPException, status, Body
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jwt.exceptions import  InvalidTokenError

http_bearer = HTTPBearer()

router = APIRouter(prefix="/jwt", tags=['JWT'])

# john = UserSchema(
#     username='john',
#     password=hash_password('qwerty'),
#     email='john@gmail.com'
# )
# sam = UserSchema(
#     username='sam',
#     password=hash_password('secret'),
# )
#
# users_db: dict[str, UserSchema] = {
#     john.username: john,
#     sam.username: sam
# }


async def validate_auth_user(
        username: str = Form(),
        password: str = Form()):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='invalid username or password')

    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive')
    return user

async def validate_auth_user(
        username: str = Form(),
        password: str = Form()):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='invalid username or password')


    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive')
    return user

async def get_curresnt_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
)->UserSchema:
    token = credentials.credentials
    print(token)
    payload = decode_jwt(token=token)
    try:
        payload = decode_jwt(token = token)


    except InvalidTokenError as e:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'invalid token error {e}')
    return payload

async def get_curresnt_auth_user(
        payload: dict = Depends(get_curresnt_token_payload)
)->UserSchema:
    username: str | None = payload.get('sub')
    if not (user := users_db.get(username)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='token invalid')
    return user





async def get_curresnt_active_auth_user(
        user: UserSchema = Depends(get_curresnt_auth_user)
):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='user inactive')


@router.post("/login/", response_model=TokenInfo)
async def auth_user(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {'sub': user.username,
                   'email': user.email}
    token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type='Bearer')


@router.get('/users/me')
async def auth_user_check(
        user: UserSchema = Depends(get_curresnt_active_auth_user)
):
    return {'username': user.username,
            'email': user.email}


@router.post('/registration/')
async def registration(user: UserModel = Body(),session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    result = await crud.registration(user=user,session=session)
    return result



