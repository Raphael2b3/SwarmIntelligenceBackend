from typing import Annotated
from fastapi import Depends, FastAPI
import models
from services.jwt_auth import get_current_active_user
from models.user import User
from models.requests import SearchRequest, CreateUserRequest
import controller

app = FastAPI()
# TODO Andere routen includieren

