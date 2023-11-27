from typing import Annotated

from fastapi import APIRouter, Depends

from db.core import Database as Db
from db.transactions import statement_create_tx, statement_delete_tx, statement_get_many_tx, statement_get_context_tx, \
    statement_vote_tx, statement_modify_tag_tx
from models import User, Statement, RequestStatementSearch, RequestStatementCreate, RequestTagSet, RequestStatementVote
from models.responses import Response, Equation
from security.jwt_auth import get_current_active_user, get_optional_user

router = APIRouter(prefix="/equation", )


@router.get("/" ,response_model=Response[Equation])
async def get(current_user: Annotated[User, Depends(get_optional_user)], id:str, limit:int, skip:int):
    print(f"GET Equation \nBy: {id}\n")
    async with Db.session() as session:
        result = await session.execute_read(equation_get_many_tx
                                            , query_string=id, n_results=limit,
                                            skip=skip)
    return result


@router.post("/", response_model=Response[Statement])
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: RequestStatementCreate):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(statement_create_tx, text=body.value,
                                        username=current_user.username)
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        id:str):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(statement_delete_tx, statement_id=id,
                                        username=current_user.username)
    return r


@router.post("/tag", response_model=Response)
async def modify_tag(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestTagSet):
    print(f"MODIFY TAG \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(statement_modify_tag_tx,
                                        username=current_user.username,
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

