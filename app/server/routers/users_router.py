
import config as con

from fastapi import APIRouter, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from app.server.crud import get_all_users, delete_some_user, update_user_information, create_new_user
from app.server.db_helper import db_helper
from app.server.schemas import UserUpdate, CreateUser

users_router = APIRouter(prefix="/users", tags=['USERS'])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, con.private_key, algorithms=[con.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except:
        raise credentials_exception
    return payload

def check_admin_role(current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

# Пример декоратора для проверки роли admin
def admin_permission_required(route_function):
    async def decorated_function(*args, **kwargs):
        check_admin_role()
        return await route_function(*args, **kwargs)
    return decorated_function

# Пример использования декоратора
@users_router.get("/list/", description='Endpoint that shows all users', response_description="List all users", response_model=list)
@admin_permission_required
async def list_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    users = await get_all_users(session)
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
    response_model_by_alias=False,)
async def create_user(user: CreateUser = Body(),
                      session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_user = await create_new_user(user, session)
    return new_user
