from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models import statement, user
from models.statement import Statement
from services.jwt_auth import get_current_active_user, get_optional_user
import controller as ctrl

router = APIRouter(prefix="/statement", )


@router.get("/", response_model=list[statement.Statement])
async def get(current_user: Annotated[user.User, Depends(get_optional_user)], q=""):
    print(f"GET STATEMENT \nBy: {current_user}\nBody: {q}")
    result = ctrl.statements.get_many(queryString=q)
    return result


@router.post("/create")
async def create(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Statement, Depends()]):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    ctrl.statements.create(text=form_data.value,username=current_user.username)


@router.post("/context", response_model=statement.Statement)
async def get_context(
        current_user: Annotated[user.User, Depends(get_optional_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"GET CONTEXT STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = ctrl.statements.get_one(form_data)
    return result


@router.post("/delete/glob", response_model=statement.Statement)
async def delete_globally(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result =  ctrl.statements.delete(form_data)
    return result


@router.post("/delete", response_model=statement.Statement)
async def delete_for_project(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[Any, Depends()]):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result =  ctrl.statements.delete(form_data)
    return result
