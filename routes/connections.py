from typing import Annotated

from fastapi import APIRouter, Depends

from models import project, user, requests, connection
from services.jwt_auth import get_current_active_user
import controller as ctrl

router = APIRouter(prefix="/connection", )


@router.post("/create", response_model=connection.Connection)  # auth
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[connection.Connection, Depends()]):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.create(form_data)
    return result


@router.post("/weight", response_model=connection.Connection)  # auth
async def weight(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[connection.Connection, Depends()]):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.create(form_data)
    return result


@router.post("/delete", response_model=connection.Connection)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"DELETE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.delete(form_data)
    return result
