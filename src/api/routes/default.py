from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import HTMLResponse
from typing_extensions import Literal

import security
from db import user_report, user_modify_star, statement_get_context, statement_calculate_truth
from api.models import *
from ..auth import authenticate_user, get_optional_user, get_current_user

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    credential = await authenticate_user(credentials.username, credentials.password)
    if credential:
        return await security.get_new_access_token(credentials=credential)


@router.post("/context", response_model=Response[Context])
async def get_context(current_user: Annotated[User, Depends(get_optional_user)], body: RequestContext):
    r = await statement_get_context(statement_id=body.id, exclude_ids=body.exclude_ids,
                                    username=current_user.username)
    return r


@router.post("/{controller}/star", response_model=Response)
async def star(controller: Literal["statement", "project", "user"],
               current_user: Annotated[User, Depends(get_current_user)],
               body: RequestStarSet):
    r = await user_modify_star(username=current_user.username, objectid=body.id,
                               _type=controller, removestar=body.value)
    return r


@router.post("/{controller}/report", response_model=Response)
async def report(controller: Literal["statement", "project", "user"],
                 body: RequestReportCreate):
    r = await user_report(objectid=body.id, _type=controller, reason=body.value)
    return r


@router.get("/updatetruth", response_model=Response)
async def update_truth():
    r = await statement_calculate_truth()
    return r


@router.get("/", response_class=HTMLResponse)
async def default():
    return """<html>
    <body>
    See documentation:
    <br/>
    <a href="https://github.com/Raphael2b3/SwarmIntelligenceBackend">GitHub Repository</a>
    <br/>
    <a href="/docs">Find Out how this api works</a>
    </body>
    </html>
    """
