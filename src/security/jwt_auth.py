from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import db
import load_env

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

env: dict


def init():
    global env
    env = load_env.load_settings_from_env("SEC___SECRET_KEY", "SEC_ALGORITHM",
                                          "SEC_ACCESS_TOKEN_EXPIRE_MINUTES")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username, password):
    hashed_pw = await db.user_get_hashed_password(username=username)
    if not hashed_pw:
        return False
    if not verify_password(password, hashed_pw):
        return False
    return username


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env["SEC___SECRET_KEY"], algorithm=env["SEC_ALGORITHM"])
    return encoded_jwt


async def get_optional_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        return await get_current_user(token)
    finally:
        return {"username": "", "hashed_password": ""}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, env["SEC___SECRET_KEY"], algorithms=[env["SEC_ALGORITHM"]])

    try:
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    db_user = await db.user_get(username=username)

    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_new_access_token(*, username, password):
    credentials = await authenticate_user(username, password)
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
