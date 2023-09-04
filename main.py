import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.dbcontroller import Database as Db
from env import HOST, PORT
from routes import default, tags, statements, users, connections


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Db.init()
    # bevor api online
    yield
    # sobald apie offline geht
    await Db.close()


app = FastAPI(lifespan=lifespan)
app.include_router(default.router)
app.include_router(tags.router)
app.include_router(statements.router)
app.include_router(users.router)
app.include_router(connections.router)

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], )

if __name__ == '__main__':
    # import tests.create_example_db, asyncio
    # asyncio.run(tests.create_example_db.main())

    uvicorn.run(app, host=HOST, port=PORT)

# TODO beim mergen von zwei Statements müssen Kreise behandelt werden

# TODO Choose the best fulltext analyzer <= Language Problem

# TODO Recommendations
