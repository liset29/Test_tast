from sqlalchemy.ext.asyncio import AsyncSession

from app.server.crud import update_role_key
from app.server.db_helper import db_helper
from app.server import crud
from app.server.utils import  encode_jwt,  validate_auth_user,get_curresnt_active_auth_user
from app.server.schemas import UserSchema, TokenInfo, UserModel, Registration, Registered
from fastapi import APIRouter, Depends,status, Body
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer()

auth_router = APIRouter(prefix="/user", tags=['USER'])


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

    result = await crud.registration(user=user, session=session)
    return result