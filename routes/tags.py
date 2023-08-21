from typing import Annotated
from fastapi import APIRouter, Depends

from models import SearchTagRequest, User, CreateTagRequest, DeleteRequest
from security.jwt_auth import get_current_active_user
from db.dbcontroller import Database as Db
from db.transactions import tag_get_many_tx, tag_create_tx,tag_delete_tx

router = APIRouter(prefix="/tag", )


@router.get("/", response_model=list[Tag])
async def get(body: SearchTagRequest):
    print(f"GET PROJECT \nBy: Anyone\nBody: {q}")
    async with Db.session() as session:
        result = await session.execute_read(tag_get_many_tx, query_string=q)
    return result


@router.post("/create")
async def create(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: CreateTagRequest):
    print(f"CREATE PROJECT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(tag_create_tx, tag=body.value,
                                    username=current_user.username)


@router.post("/delete")
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: DeleteRequest):
    print(f"DELETE PROJECT \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        await session.execute_write(tag_delete_tx, tag=body.id,
                                    username=current_user.username)
