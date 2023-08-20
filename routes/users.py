from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

import services.jwt_auth
from models import user
from models.user import CreateUserRequest
from services.dbcontroller import get_driver
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/user", )


@router.post("/create")
async def create(
        body: CreateUserRequest):
    print(f"CREATE USER \nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(db.users.user_create_tx, username=body.username, hashed_password=services.jwt_auth.get_password_hash(body.password))



@router.post("/delete")
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)]):
    print(f"DELETE USER \nBy: {current_user}\nBody: {current_user}")
    async with get_driver().session(database="neo4j") as session:
        result = await session.execute_write(db.users.delete_user_tx, username=current_user.username)
    return result
