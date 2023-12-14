from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from security import pwd_context

import db

import security.jwt as jwt


async def authenticate_user(username, password):
    hashed_pw = await db.user_get_hashed_password(username=username)
    if not hashed_pw:
        return False
    if not pwd_context.verify(password, hashed_pw):
        return False
    return username


async def get_current_user(token: Annotated[str, Depends(jwt.oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = get_token_data(token)
    except:
        raise credentials_exception

    db_user = await db.user_get(username=username)

    if db_user is None: raise credentials_exception

    return db_user


async def get_optional_user(token: Annotated[str, Depends(get_current_user)]):
    try:
        return await get_token_data(token)
    finally:
        return {"username": "", "hashed_password": ""}
