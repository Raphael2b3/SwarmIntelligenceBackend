from typing import Annotated

from fastapi import APIRouter, Depends

from db.dbcontroller import Database as Db
from db.transactions import connection_create_tx, connection_delete_tx, connection_weight_tx
from models import User, RequestConnectionCreate, RequestConnectionVote, RequestDelete
from security.jwt_auth import get_current_active_user

router = APIRouter(prefix="/connection", )


@router.post("/create")
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: RequestConnectionCreate):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {body}")

    async with Db.session() as session:
        await session.execute_write(connection_create_tx, start_id=body.child_id,
                                    stopId=body.parent_id,
                                    supports=body.supports,
                                    username=current_user.username)


@router.post("/vote")  # auth
async def weight(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestConnectionVote):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(
            connection_weight_tx, connection_id=body.id,
            is_bad=body.value,
            username=current_user.username)


@router.post("/delete")
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestDelete):
    print(f"DELETE CONNECTION \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(
            connection_delete_tx, connection_id=body.id,
            username=current_user.username)
