from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import load_env

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

env: dict


def init():
    global env
    env = load_env.load_settings_from_env("SEC___SECRET_KEY", "SEC_ALGORITHM",
                                          "SEC_ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env["SEC___SECRET_KEY"], algorithm=env["SEC_ALGORITHM"])
    return encoded_jwt


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, env["SEC___SECRET_KEY"], algorithms=[env["SEC_ALGORITHM"]])
    sub = payload.get("sub")
    if sub is None:
        raise
    return sub


async def get_new_access_token(*, credentials):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(env["SEC_ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": credentials}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
