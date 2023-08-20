from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models import statement, user
from models.context import ContextRequest, StatementContext
from models.statement import Statement
from services.dbcontroller import get_driver
from services.jwt_auth import get_current_active_user, get_optional_user
import controller as ctrl

router = APIRouter(prefix="/statement", )


@router.get("/", response_model=list[statement.Statement])
async def get(current_user: Annotated[user.User, Depends(get_optional_user)], q=""):
    print(f"GET STATEMENT \nBy: {current_user}\nBody: {q}")
    async with get_driver().session(database="neo4j") as session:
        result = await session.execute_read(ctrl.statements.statement_get_many_tx, queryString=q,
                                            username=current_user.username)
    return result


@router.post("/create")
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: Statement):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        t = await session.execute_write(ctrl.statements.statement_create_tx, text=body.value,
                                        username=current_user.username)
        print(t)


@router.post("/context", response_model=StatementContext)
async def get_context(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        body: ContextRequest):
    print(f"GET CONTEXT STATEMENT \nBy: {current_user}\nBody: {body}")

    async with get_driver().session(database="neo4j") as session:
        await session.execute_read(ctrl.statements.statement_get_context_tx, statementId=body.id,
                                   username=current_user.username,
                                   n_parents=body.n_parents,
                                   skip_parents=body.skip_parents,
                                   skip_children=body.skip_childs,
                                   n_children=body.n_childs,
                                   childgenerations=body.childgenerations,
                                   parentgenerations=body.parentgenerations)


@router.post("/delete", response_model=statement.Statement)
async def delete_globally(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: Any):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(ctrl.statements.statement_delete_tx, statementId=body.id,
                                    username=current_user.username)


class TagRequest(BaseModel):
    id: str
    project: str
    remove: bool


@router.post("/tag", response_model=statement.Statement)
async def delete_for_project(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: TagRequest):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(ctrl.statements.statement_modify_project_tag_tx, username=current_user.username,
                                    statementId=body.id, project=body.project, remove=body.remove)
