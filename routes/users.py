from typing import Annotated

from fastapi import APIRouter, Depends

from db.dbcontroller import Database as Db
from db.transactions import user_create_tx, user_delete_tx
from models import User, RequestUserCreate
from security.jwt_auth import get_current_active_user, get_password_hash

router = APIRouter(prefix="/user", )


@router.post("/create")
async def create(
        body: RequestUserCreate):
    print(f"CREATE USER \nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(user_create_tx,
                                    username=body.username, hashed_password=get_password_hash(body.password))


@router.post("/delete")
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    async with Db.session() as session:
        await session.execute_write(user_delete_tx, username=current_user.username)
