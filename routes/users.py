from typing import Annotated

from fastapi import APIRouter, Depends
from models import user, requests
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/user", )


@router.post("/", response_model=list[user.User])
async def get_user(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"GET USER \nBy: {current_user}\nBody: {form_data}")
    result = db.users.get_many(form_data)
    return result


@router.post("/create")
async def create_user(
        form_data: Annotated[requests.CreateUserRequest, Depends()]):
    print(f"CREATE USER \nBody: {form_data}")
    result = db.users.create(form_data)

    return 200 if result else 500


@router.post("/select", response_model=user.User)
async def select_user(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"SELECT USER \nBy: {current_user}\nBody: {form_data}")
    result = db.users.get_one(form_data)
    return result


@router.post("/delete", response_model=user.User)
async def delete_user(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {form_data}")
    result = db.users.delete(form_data)
    return result

# TODO Test Every api endpoint