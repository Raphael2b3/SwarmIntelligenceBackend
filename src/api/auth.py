from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

import db
import security


async def authenticate_user(username, password):
    hashed_pw = await db.user_get_hashed_password(username=username)
    if not hashed_pw:
        return False
    if not security.pwd_context.verify(password, hashed_pw):
        return False
    return username


async def get_current_user(token: Annotated[str, Depends(security.oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: username = security.get_token_data(token)
    except: raise credentials_exception

    db_user = await db.user_get(username=username)

    if db_user is None: raise credentials_exception

    return db_user


async def get_optional_user(token: Annotated[str, Depends(get_current_user)]):
    try:
        return await security.get_token_data(token)
    finally:
        return {"username": "", "hashed_password": ""}
