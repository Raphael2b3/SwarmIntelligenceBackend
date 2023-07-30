from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
import models
from routes import *
from services.jwt_auth import get_current_active_user
from models.user import User
from models.requests import SearchRequest, CreateUserRequest
import controller

app = FastAPI()
app.include_router(default.router)
app.include_router(projects.router)
app.include_router(statements.router)
app.include_router(users.router)


if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=5555)