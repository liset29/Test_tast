import asyncio
from app.server.database import init_models
import uvicorn


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("app.server.app:app", host="127.0.0.1", port=8000, reload=True)

