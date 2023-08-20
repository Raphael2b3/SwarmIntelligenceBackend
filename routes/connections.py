from typing import Annotated, Any

from fastapi import APIRouter, Depends

from models import project, user, connection
from services.dbcontroller import get_driver
from services.jwt_auth import get_current_active_user
import controller as ctrl

router = APIRouter(prefix="/connection", )


@router.post("/create")
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: connection.Connection):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(ctrl.connections.connection_create_tx, startId=body.stm_start,
                                    stopId=body.stm_stop,
                                    supports=body.supports,
                                    username=current_user.username)


@router.post("/isbad")  # auth
async def weight(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: connection.Connection):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(
            ctrl.connections.connection_weight_tx, connectionId=body.id,
            is_bad=body.is_bad,
            username=current_user.username)


@router.post("/delete")
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: Any):
    print(f"DELETE CONNECTION \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(
            ctrl.connections.connection_delete_tx, connectionId=body.id,
            username=current_user.username)
