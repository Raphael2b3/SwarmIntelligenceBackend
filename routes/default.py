from datetime import timedelta
from typing import Annotated, Any

from pydantic import BaseModel
from typing_extensions import Literal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from db.dbcontroller import Database as Db
from db.transactions import user_report_tx, user_modify_star_tx
from models import CreateReportRequest, User, SetStarRequest
from security.jwt_auth import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    credentials = await authenticate_user(credentials)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": credentials}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("{controller}/star")
async def star(controller: Literal["statement", "project", "user",],
               current_user: Annotated[User, Depends(get_current_active_user)],
               body: SetStarRequest):
    async with Db.session() as session:
        await session.execute_write(
            user_modify_star_tx, username=current_user.username, objectid=body.id,
            _type=controller, removestar=body.value)


@router.post("{controller}/report")
async def report(controller: Literal["statement", "project", "user"],
                 body: CreateReportRequest):
    async with Db.session() as session:
        await session.execute_write(
            user_report_tx, objectid=body.id, _type=controller, reason=body.value)
