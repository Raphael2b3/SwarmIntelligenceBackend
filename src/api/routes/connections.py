from typing import Annotated
from fastapi import APIRouter, Depends
from db import connection_create, connection_weight, connection_delete
from security import get_current_active_user
from api.models import *
router = APIRouter(prefix="/connection")


@router.post(path="", response_model=Response[Connection])
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: RequestConnectionCreate):
    r = await connection_create(start_id=body.child_id,
                                stop_id=body.parent_id,
                                is_support=body.supports,
                                username=current_user.username)
    return r


@router.post("/vote", response_model=Response)
async def weight(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestConnectionVote):
    r = await connection_weight(connection_id=body.id,
                                weight=body.value,
                                username=current_user.username)
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        id: str = ""):
    r = await connection_delete(connection_id=id,
                                username=current_user.username)
    return r
