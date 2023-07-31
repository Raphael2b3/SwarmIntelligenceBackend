from typing import Annotated

from fastapi import APIRouter, Depends
from models import project, user, requests,connection
from services.jwt_auth import get_current_active_user
import controller as ctrl

router = APIRouter(prefix="/connection", )


@router.post("/", response_model=list[connection.Connection])
async def get(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"GET CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.get_many(form_data)
    return result


@router.post("/create", response_model=connection.Connection)
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[connection.Connection, Depends()]):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.create(form_data)
    return result


@router.post("/select", response_model=connection.Connection)
async def select(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"SELECT CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.get_one(form_data)
    return result


@router.post("/delete", response_model=connection.Connection)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"DELETE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.delete(form_data)
    return result
