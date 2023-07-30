from typing import Annotated

from fastapi import APIRouter, Depends
from models import project, user, requests
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/project", )


@router.post("/", response_model=list[project.Project])
async def get(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"GET PROJECT \nBy: {current_user}\nBody: {form_data}")
    result = db.projects.get_many(form_data)
    return result


@router.post("/create", response_model=project.Project)
async def create_project(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"CREATE PROJECT \nBy: {current_user}\nBody: {form_data}")
    result = db.projects.create(form_data)
    return result


@router.post("/select", response_model=project.Project)
async def select_project(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"SELECT PROJECT \nBy: {current_user}\nBody: {form_data}")
    result = db.projects.get_one(form_data)
    return result


@router.post("/delete", response_model=project.Project)
async def delete_project(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"DELETE PROJECT \nBy: {current_user}\nBody: {form_data}")
    result = db.projects.delete(form_data)
    return result
