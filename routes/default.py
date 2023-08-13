from datetime import timedelta
from typing import Annotated, Any
from typing_extensions import Literal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import user
from models.report import Report
from services.jwt_auth import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
from controller.users import report, modify_star

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    username = authenticate_user(form_data)
    if not user:
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
               form_data: Annotated[Any, Depends()], remove: bool = False, ):
    return controller + modify_star(current_user, form_data, remove)


@router.post("{controller}/report")
async def report_model(_controller: Literal["statement", "project", "user"],
                       form_data: Annotated[Report, Depends()]):
    return _controller + report(form_data, _controller)
