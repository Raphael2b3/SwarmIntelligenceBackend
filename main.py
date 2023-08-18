from pydantic import BaseConfig

from const import HOST, PORT
import uvicorn
from fastapi import Depends, FastAPI
from routes import default, projects, statements, users, connections

app = FastAPI()
app.include_router(default.router)
app.include_router(projects.router)
app.include_router(statements.router)
app.include_router(users.router)
app.include_router(connections.router)

if __name__ == '__main__':
    import services.dbcontroller as db
    db.init()

    uvicorn.run(app, host=HOST, port=int(PORT))

    db.teardown()