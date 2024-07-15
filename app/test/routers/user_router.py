from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.test.database import get_session
from app.test.schemas import UserResponse, UserCreate
from app.test import crud

router = APIRouter()

@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db=db, user=user)

@router.get("/")
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    users = await crud.get_users(db)
    return users

@router.get("/{username}")
async def read_user(username: str, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
