from typing import Annotated

from fastapi import APIRouter, Depends
from models import statement, user, requests
from services.jwt_auth import get_current_active_user
import controller as db

router = APIRouter(prefix="/statement", )


@router.post("/", response_model=list[statement.Statement])
async def get_statement(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"GET STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.get_many(form_data)
    return result


@router.post("/create", response_model=statement.Statement)
async def create_statement(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"CREATE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.create(form_data)
    return result


@router.post("/select", response_model=statement.Statement)
async def select_statement(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"SELECT STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.get_one(form_data)
    return result


@router.post("/delete", response_model=statement.Statement)
async def delete_statement(
        current_user: Annotated[user.User, Depends(get_current_active_user)],
        form_data: Annotated[requests.SearchRequest, Depends()]):
    print(f"DELETE STATEMENT \nBy: {current_user}\nBody: {form_data}")
    result = db.statements.delete(form_data)
    return result
