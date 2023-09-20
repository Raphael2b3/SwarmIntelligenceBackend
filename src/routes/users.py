from typing import Annotated

from fastapi import APIRouter, Depends

from db.dbcontroller import Database as Db
from db.transactions import user_create_tx, user_delete_tx, user_change_password_tx
from models import User, RequestUserCreate, RequestUserPasswordChange
from models.responses import Response
from security.jwt_auth import get_current_active_user, get_password_hash, authenticate_user

router = APIRouter(prefix="/user", )


@router.post("/", response_model=Response)
async def create(
        body: RequestUserCreate):
    print(f"CREATE USER \nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(user_create_tx,
                                        username=body.username, hashed_password=get_password_hash(body.password))
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    async with Db.session() as session:
        r = await session.execute_write(user_delete_tx, username=current_user.username)
    return r


@router.put("/", response_model=Response)
async def change_password(
        current_user: Annotated[User, Depends(get_current_active_user)], body: RequestUserPasswordChange):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")

    if not await authenticate_user(current_user.username, body.old):
        return Response(message="the old password is not correct")

    async with Db.session() as session:
        r = await session.execute_write(user_change_password_tx, username=current_user.username,
                                        password=get_password_hash(body.new))
    return r
