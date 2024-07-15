from fastapi import FastAPI
from app.test.routers import user_router, auth_router
from app.test.database import engine
from app.test.models import Base

app = FastAPI()

# Создание таблиц
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Hello World"}