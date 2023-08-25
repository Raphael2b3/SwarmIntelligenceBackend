from typing import Annotated

from fastapi import APIRouter, Depends

from db.dbcontroller import Database as Db
from db.transactions import user_create_tx, user_delete_tx, user_changepassword_tx
from models import User, RequestUserCreate, RequestUserPasswordChange
from security.jwt_auth import get_current_active_user, get_password_hash

router = APIRouter(prefix="/user", )


@router.post("/create")
async def create(
        body: RequestUserCreate):
    print(f"CREATE USER \nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(user_create_tx,
                                        username=body.username, hashed_password=get_password_hash(body.password))
    return r


@router.post("/delete")
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    async with Db.session() as session:
        r = await session.execute_write(user_delete_tx, username=current_user.username)
    return r


@router.post("/changepassword")
async def change_password(
        current_user: Annotated[User, Depends(get_current_active_user)],body: RequestUserPasswordChange):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    async with Db.session() as session:
        r = await session.execute_write(user_changepassword_tx, username=current_user.username,password=body.value)
    return r
