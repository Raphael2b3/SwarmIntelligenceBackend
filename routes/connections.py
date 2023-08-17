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
    ctrl.connections.create_connection(startId=form_data.stm_start,
                                       stopId=form_data.stm_stop,
                                       supports=form_data.supports,
                                       username=current_user.username)


@router.post("/is_bad")  # auth
async def weight(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[connection.Connection, Depends()]):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    ctrl.connections.weight_connection(connectionId=form_data.id,
                                       is_bad=form_data.is_bad,
                                       username=current_user.username)


@router.post("/delete")
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"DELETE CONNECTION \nBy: {current_user}\nBody: {form_data}")
    ctrl.connections.delete_connection(connectionId=form_data.id,
                                                username=current_user.username)
