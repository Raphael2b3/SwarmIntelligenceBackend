from datetime import timedelta
from typing import Annotated, Any

from pydantic import BaseModel
from typing_extensions import Literal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import user
from models.report import Report
from services.dbcontroller import get_driver
from services.jwt_auth import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
import controller as cntrl

router = APIRouter()


class Kok(BaseModel):
    username: str
    password: str


def test(*args):
    print(*args)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[Any, Depends(OAuth2PasswordRequestForm)]):
    username = await authenticate_user(form_data)
    print("username_", username)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("{controller}/star")
async def star(controller: Literal["statement", "project", "user",],
               current_user: Annotated[user.User, Depends(get_current_active_user)],
               body: Any):
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(
            cntrl.users.user_modify_star_tx, username=current_user.username, objectid=body.id,
            _type=controller, removestar=body.remove)


@router.post("{controller}/report")
async def report(controller: Literal["statement", "project", "user"],
                 body: Report):
    async with get_driver().session(database="neo4j") as session:
        await session.execute_write(
            cntrl.users.report_tx, objectid=body.id, _type=controller, reason=body.message)
