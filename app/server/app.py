
from fastapi import FastAPI,Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.server.routers.user_router import router

app = FastAPI(title='Shop')
app.include_router(router)


#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content=jsonable_encoder({"detail": 'Incorect dataвыпваыпвы'}), )









# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.database import get_session
# from app.schemas import User, UserCreate
# from app import crud
#
# router = APIRouter()
#
# @router.post("/", response_model=User)
# async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
#     db_user = await crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return await crud.create_user(db=db, user=user)
#
# @router.get("/", response_model=list[User])
# async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
#     users = await crud.get_users(db)
#     return users
#
# @router.get("/{username}", response_model=User)
# async def read_user(username: str, db: AsyncSession = Depends(get_session)):
#     db_user = await crud.get_user_by_username(db, username=username)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
