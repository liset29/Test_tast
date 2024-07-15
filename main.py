import asyncio
from app.server.database import init_models
import uvicorn
# from app.test.app import init_models

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("app.server.app:app", host="127.0.0.1", port=8000, reload=True)


# if __name__ == "__main__":
#     asyncio.run(init_models())
#
#     uvicorn.run("app.test.app:app", host="127.0.0.1", port=8000, reload=True)