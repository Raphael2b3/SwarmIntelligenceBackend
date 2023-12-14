from typing import Annotated

from fastapi import APIRouter, Depends

from db import tag_get_many, tag_create, tag_delete
from models import *
from security.auth import get_current_user

router = APIRouter(prefix="/tag", )


@router.get("/", response_model=Response[list[Tag]])
async def get(q: str = "", results: int = 10, skip: int = 0):
    result = await tag_get_many(query_string=q, n_results=results,
                                skip=skip)
    return result


@router.post("/", response_model=Response[Tag])
async def create(
        current_user: Annotated[User, Depends(get_current_user)],
        body: RequestTagCreate):
    r = await tag_create(tag=body.value,
                         username=current_user.username)
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_user)],
        id: str = ""):
    r = await tag_delete(tag=id,
                         username=current_user.username)
    return r
