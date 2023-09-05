from typing import Annotated

from fastapi import APIRouter, Depends

from db.dbcontroller import Database as Db
from db.transactions import tag_get_many_tx, tag_create_tx, tag_delete_tx
from models import RequestTagSearch, User, RequestTagCreate, RequestDelete, Tag
from models.responses import Response
from security.jwt_auth import get_current_active_user

router = APIRouter(prefix="/tag", )


@router.post("/", response_model=Response[list[Tag]])
async def get(body: RequestTagSearch):
    print(f"GET TAG \nBy: Anyone\nBody: {body}")
    async with Db.session() as session:
        result = await session.execute_read(tag_get_many_tx, query_string=body.q)
    return result


@router.post("/create", response_model=Response[Tag])
async def create(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestTagCreate):
    print(f"CREATE TAG \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(tag_create_tx, tag=body.value,
                                        username=current_user.username)
    return r


@router.post("/delete", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestDelete):
    print(f"DELETE TAG \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(tag_delete_tx, tag=body.id,
                                        username=current_user.username)
    return r
