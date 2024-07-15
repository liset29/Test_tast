from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.test.models import User
from app.test.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def get_users(db: AsyncSession):
    result = await db.execute(select(User).order_by(User.id))
    return result.scalars().all()
