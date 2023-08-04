from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models import user
from models.user import CreateUserRequest
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/user", )


@router.post("/create")
async def create(
        form_data: Annotated[CreateUserRequest, Depends()]):
    print(f"CREATE USER \nBody: {form_data}")
    result = db.users.create(form_data)
    return result


@router.post("/delete", response_model=user.User)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    result = db.users.delete(current_user)
    return result
