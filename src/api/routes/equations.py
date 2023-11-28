from typing import Annotated

from fastapi import APIRouter, Depends

from db import statement_create, statement_delete, statement_get_many, statement_get_context, \
    statement_vote, statement_modify_tag
from security import get_current_active_user, get_optional_user
from models import *
router = APIRouter(prefix="/equation")


@router.get("/", response_model=Response[Equation])
async def get(current_user: Annotated[User, Depends(get_optional_user)], id: str, limit: int, skip: int):

    result = await equation_get_many(query_string=id, n_results=limit,
                                     skip=skip)
    return result


@router.post("/", response_model=Response[Statement])
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: RequestStatementCreate):
    r = await statement_create(text=body.value,
                               username=current_user.username)
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        id: str):
    r = await statement_delete(statement_id=id,
                               username=current_user.username)
    return r


@router.post("/tag", response_model=Response)
async def modify_tag(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestTagSet):
    r = await statement_modify_tag(username=current_user.username,
                                   statement_id=body.id, tags=body.tags)
    return r


@router.post("/vote", response_model=Response)
async def vote(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestStatementVote):
    print(f"VOTE STATEMENT \nBy: {current_user}")
    async with Db.session() as session:
        r = await session.execute_write(et,
                                        username=current_user.username,
                                        statement_id=body.id, vote=body.value)
    return r
