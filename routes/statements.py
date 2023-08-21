from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from db.dbcontroller import Database as Db

from db.transactions import statement_create_tx, statement_delete_tx, statement_get_many_tx, statement_get_context_tx, \
    statement_vote_tx, statement_modify_tag_tx
from models import User, StatementResponse, SearchStatementRequest, CreateStatementRequest, ContextResponse, \
    ContextRequest, \
    DeleteRequest, SetTagRequest, VoteStatementRequest
from security.jwt_auth import get_current_active_user, get_optional_user

router = APIRouter(prefix="/statement", )


@router.post("/", response_model=list[StatementResponse])
async def get(current_user: Annotated[User, Depends(get_optional_user)], body: SearchStatementRequest):
    print(f"GET STATEMENT \nBy: {current_user}\nBody: {q}")
    async with Db.session() as session:
        result = await session.execute_read(statement_get_many_tx, query_string=body.q,
                                            username=current_user.username)
    return result


@router.post("/create")
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: CreateStatementRequest):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(statement_create_tx, text=body.value,
                                    username=current_user.username)


@router.post("/context", response_model=ContextResponse)
async def get_context(current_user: Annotated[User, Depends(get_optional_user)], body: ContextRequest):
    print(f"GET CONTEXT STATEMENT \nBy: {current_user}\nBody: {body}")

    async with Db.session() as session:
        await session.execute_read(statement_get_context_tx, statement_id=body.id, exclude_ids=body.exclude_ids, )


@router.post("/delete", )
async def delete_globally(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: DeleteRequest):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(statement_delete_tx, statement_id=body.id,
                                    username=current_user.username)


@router.post("/tag")
async def modify_tag(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: SetTagRequest):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(statement_modify_tag_tx,
                                    username=current_user.username,
                                    statement_id=body.id, tags=body.tags)


@router.post("/vote")
async def vote(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: VoteStatementRequest):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(statement_vote_tx,
                                    username=current_user.username,
                                    statement_id=body.id, vote=body.value)
