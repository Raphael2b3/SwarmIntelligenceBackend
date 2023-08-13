from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models import statement, user
from services.jwt_auth import get_current_active_user, get_optional_user
import controller as db

router = APIRouter(prefix="/statement", )


@router.post("/", response_model=statement.Statement)
async def get(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"GET STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.get_many(form_data)
    return result


@router.post("/create", response_model=statement.Statement)
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.create(form_data)
    return result


@router.post("/context", response_model=statement.Statement)
async def get_context(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"GET CONTEXT STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.get_one(form_data)
    return result


@router.post("/delete/glob", response_model=statement.Statement)
async def delete_globally(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.delete(form_data)
    return result

@router.post("/delete", response_model=statement.Statement)
async def delete_for_project(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.delete(form_data)
    return result