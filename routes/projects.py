from typing import Annotated
from fastapi import APIRouter, Depends
from models import project, user
from models.project import ProjectQuery
from services.jwt_auth import get_optional_user, get_current_active_user
import controller as ctrl

router = APIRouter(prefix="/project", )


@router.get("/", response_model=list[project.Project])
async def get(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        q=""):
    print(f"GET PROJECT \nBy: Anyone\nBody: {q}")
    result = ctrl.projects.get_many(queryString=q)
    return result


@router.post("/create")
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[project.Project, Depends()]):
    print(f"CREATE PROJECT \nBy: {current_user}\nBody: {form_data}")
    ctrl.projects.create(username=current_user.username,projectname=form_data.name)


@router.post("/delete")
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[project.Project, Depends()]):
    print(f"DELETE PROJECT \nBy: {current_user}\nBody: {form_data}")
    ctrl.projects.delete(projectname=form_data.name, username=current_user.username)

