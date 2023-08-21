from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from db.dbcontroller import Database as Db
from env import HOST, PORT
from routes import default, tags, statements, users, connections


@asynccontextmanager
async def lifespan(app: FastAPI):
    Db.init()
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

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)

#  TODO variablen Benennung, code refactoring

#  TODO doku überarbeiten/ generieren lassen durch uvicorn


# TODO beim mergen von zwei Statements müssen Kreise behandelt werden
