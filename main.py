from contextlib import contextmanager, asynccontextmanager
import services.dbcontroller as db
from const import HOST, PORT
import uvicorn
from fastapi import Depends, FastAPI
from routes import default, projects, statements, users, connections


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    # bevor api online
    yield
    # sobald apie offline geht
    await db.get_driver().close()


app = FastAPI(lifespan=lifespan)
app.include_router(default.router)
app.include_router(projects.router)
app.include_router(statements.router)
app.include_router(users.router)
app.include_router(connections.router)

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)

#  TODO variablen Benennung, code refactoring

#  TODO doku überarbeiten/ generieren lassen durch uvicorn
