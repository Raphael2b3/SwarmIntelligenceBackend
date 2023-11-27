from typing import Annotated

from fastapi import APIRouter, Depends

from db.core import Database as Db
from db.transactions import tag_get_many_tx, tag_create_tx, tag_delete_tx
from models import User, RequestTagCreate, Tag
from models.responses import Response
from security.jwt_auth import get_current_active_user

router = APIRouter(prefix="/tag", )


@router.get("/", response_model=Response[list[Tag]])
async def get(q: str = "", results: int = 10, skip: int = 0):
    print(f"GET TAG \nBy: Anyone\nq:str, results:int = 10, skip:int = 0", q, results, skip)
    async with Db.session() as session:
        result = await session.execute_read(tag_get_many_tx, query_string=q, n_results=results,
                                            skip=skip)
    return result


@router.post("/", response_model=Response[Tag])
async def create(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestTagCreate):
    print(f"CREATE TAG \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(tag_create_tx, tag=body.value,
                                        username=current_user.username)
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        id: str = ""):
    print(f"DELETE TAG \nBy: {current_user}\nid: {id}")
    async with Db.session() as session:
        r = await session.execute_write(tag_delete_tx, tag=id,
                                        username=current_user.username)
    return r
