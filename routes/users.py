from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

import services.jwt_auth
from models import user
from models.user import CreateUserRequest
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/user", )


@router.post("/create")
async def create(
        form_data: Annotated[CreateUserRequest, Depends()]):
    print(f"CREATE USER \nBody: {form_data}")
    result = db.users.create(username=form_data.username,
                             hashed_password=services.jwt_auth.get_password_hash(form_data.password))
    return result


@router.post("/delete", response_model=user.User)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    result = db.users.delete(username=current_user.username)
    return result
