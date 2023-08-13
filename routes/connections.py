from typing import Annotated, Any

from fastapi import APIRouter, Depends

from models import project, user, connection
from services.jwt_auth import get_current_active_user
import controller as ctrl

router = APIRouter(prefix="/connection", )


@router.post("/create")
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[connection.Connection, Depends()]):

    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    ctrl.connections.create_connection(form_data, current_user)


@router.post("/weight", response_model=connection.Connection)  # auth
async def weight(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[connection.Connection, Depends()]):

    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.weight_connection(form_data, current_user)

    return result


@router.post("/delete", response_model=connection.Connection)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"DELETE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.connections.delete_connection(form_data, user)
    return result
