from typing import Annotated
from fastapi import APIRouter, Depends
from models import project, user
from models.project import ProjectQuery
from services.jwt_auth import get_optional_user, get_current_active_user
import controller as db

router = APIRouter(prefix="/project", )


@router.post("/", response_model=list[project.Project])
async def get(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        form_data: Annotated[ProjectQuery, Depends()]):
    print(f"GET PROJECT \nBy: Anyone\nBody: {form_data}")
    result = db.projects.get_many(form_data, current_user)
    return result


@router.post("/create", response_model=project.Project)
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[project.Project, Depends()]):
    print(f"CREATE PROJECT \nBy: {current_user}\nBody: {form_data}")
    result = db.projects.create(form_data, current_user)
    return result


@router.post("/delete", response_model=project.Project)
async def delete(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[project.Project, Depends()]):
    print(f"DELETE PROJECT \nBy: {current_user}\nBody: {form_data}")
    result = db.projects.delete(form_data, current_user)
    return result
