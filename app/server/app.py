

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.server.routers.auth_router import auth_router
from app.server.routers.users_router import users_router

app = FastAPI(title='TEST_TASK')
app.include_router(auth_router)
app.include_router(users_router)




@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": 'Incorect data'}), )
