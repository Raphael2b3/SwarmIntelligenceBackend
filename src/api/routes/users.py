from typing import Annotated

from fastapi import APIRouter, Depends

from db import user_create, user_delete, user_change_password
from api.models import *
from ..auth import get_current_user, authenticate_user
from security import pwd_context
router = APIRouter(prefix="/user", )


@router.post("/", response_model=Response)
async def create(
        body: RequestUserCreate):
    r = await user_create(
        username=body.username, hashed_password=pwd_context.hash(body.password))
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_user)]):
    r = await user_delete(username=current_user.username)
    return r


@router.put("/", response_model=Response)
async def change_password(
        current_user: Annotated[User, Depends(get_current_user)], body: RequestUserPasswordChange):
    if not await authenticate_user(current_user.username, body.old):
        return Response(message="the old password is not correct")

    r = await user_change_password(username=current_user.username,
                                   password=pwd_context.hash(body.new))
    return r
