from typing import Annotated
from fastapi import APIRouter, Depends
from models import project, user
from models.project import ProjectQuery
from services.dbcontroller import get_driver
from services.jwt_auth import get_optional_user, get_current_active_user
import controller as ctrl

router = APIRouter(prefix="/project", )


@router.get("/", response_model=list[project.Project])
async def get(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        q=""):
    print(f"GET PROJECT \nBy: Anyone\nBody: {q}")
    async with get_driver().session(database="neo4j") as session:
        result = await session.execute_read(ctrl.projects.project_get_many, queryString=q)
    return result


@router.post("/create")
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: project.Project):
    print(f"CREATE PROJECT \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(ctrl.projects.create_project_tx, projectname=body.name,
                             username=current_user.username)


@router.post("/delete")
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        body: project.Project):
    print(f"DELETE PROJECT \nBy: {current_user}\nBody: {body}")
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(ctrl.projects.delete_project_tx, projectname=body.name,
                             username=current_user.username)
