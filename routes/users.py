from typing import Annotated

from fastapi import APIRouter, Depends
from models import user, requests
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/user", )


@router.post("/",response_model=user.User)
async def get_user(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"GET USER \nBy: {current_user}\nBody: {form_data}")
    result = db.users.get_many(form_data)
    return 0


@router.post("/create",response_model=user.User)
async def create(
        form_data: Annotated[requests.CreateUserRequest, Depends()]):
    print(f"CREATE USER \nBody: {form_data}")
    result = db.users.create(form_data)

    return 200 if result else 500


@router.post("/delete",response_model=user.User)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    result = db.users.delete(current_user)
    return 0
