from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Literal

from db.dbcontroller import Database as Db
from db.transactions import user_report_tx, user_modify_star_tx, statement_get_context_tx,statement_calculate_truth_tx
from models import RequestReportCreate, User, RequestStarSet, RequestContext
from models.responses import Response, Context
from security.jwt_auth import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user, get_optional_user

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    credentials = await authenticate_user(credentials.username, credentials.password)
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


@router.post("/context", response_model=Response[Context])
async def get_context(current_user: Annotated[User, Depends(get_optional_user)], body: RequestContext):
    print(f"GET CONTEXT STATEMENT \nBy: {current_user}\nBody: {body}")

    async with Db.session() as session:
        r = await session.execute_read(statement_get_context_tx, statement_id=body.id, exclude_ids=body.exclude_ids,
                                       username=current_user.username)
    return r


@router.post("/{controller}/star", response_model=Response)
async def star(controller: Literal["statement", "project", "user"],
               current_user: Annotated[User, Depends(get_current_active_user)],
               body: RequestStarSet):
    async with Db.session() as session:
        r = await session.execute_write(
            user_modify_star_tx, username=current_user.username, objectid=body.id,
            _type=controller, removestar=body.value)
    return r


@router.post("/{controller}/report", response_model=Response)
async def report(controller: Literal["statement", "project", "user"],
                 body: RequestReportCreate):
    async with Db.session() as session:
        r = await session.execute_write(
            user_report_tx, objectid=body.id, _type=controller, reason=body.value)
    return r


@router.get("/updatetruth", response_model=Response)
async def report():
    async with Db.session() as session:
        r = await session.execute_write(statement_calculate_truth_tx)
    return r

@router.get("/")
async def report():
    return "Hallo was geht Lukas"
