from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from security import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(prefix="project", )




