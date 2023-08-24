from typing import Annotated

from fastapi import APIRouter, Depends

from db.dbcontroller import Database as Db
from db.transactions import statement_create_tx, statement_delete_tx, statement_get_many_tx, statement_get_context_tx, \
    statement_vote_tx, statement_modify_tag_tx
from models import User, ResponseStatement, RequestStatementSearch, RequestStatementCreate, ResponseContext, \
    RequestContext, \
    RequestDelete, RequestTagSet, RequestStatementVote
from security.jwt_auth import get_current_active_user, get_optional_user

router = APIRouter(prefix="/statement", )


@router.post("/", response_model=list[ResponseStatement])
async def get(current_user: Annotated[User, Depends(get_optional_user)], body: RequestStatementSearch):
    print(f"GET STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        result = await session.execute_read(statement_get_many_tx, query_string=body.q,)
    return result


@router.post("/create")
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: RequestStatementCreate):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r=await session.execute_write(statement_create_tx, text=body.value,
                                    username=current_user.username)
    return r

@router.post("/context", response_model=ResponseContext)
async def get_context(current_user: Annotated[User, Depends(get_optional_user)], body: RequestContext):
    print(f"GET CONTEXT STATEMENT \nBy: {current_user}\nBody: {body}")

    async with Db.session() as session:
        r=await session.execute_read(statement_get_context_tx, statement_id=body.id, exclude_ids=body.exclude_ids, )
    return r

@router.post("/delete", )
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestDelete):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(statement_delete_tx, statement_id=body.id,
                                    username=current_user.username)
    return r

@router.post("/tag")
async def modify_tag(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestTagSet):
    print(f"MODIFY TAG \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r=await session.execute_write(statement_modify_tag_tx,
                                    username=current_user.username,
                                    statement_id=body.id, tags=body.tags)
    return r

@router.post("/vote")
async def vote(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestStatementVote):
    print(f"VOTE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r=await session.execute_write(statement_vote_tx,
                                    username=current_user.username,
                                    statement_id=body.id, vote=body.value)
    return r