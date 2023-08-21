from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from db.dbcontroller import Database as Db
from db.transactions import user_get_hashed_password_tx, user_get_tx
from env import __SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(userdata):
    async with Db.session() as session:
        hashed_pw = await session.execute_read(user_get_hashed_password_tx, username=userdata.username)

    if not hashed_pw:
        return False
    if not verify_password(userdata.password, hashed_pw):
        return False
    return userdata.username


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, __SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_optional_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        return await get_current_user(token)
    finally:
        return User()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, __SECRET_KEY, algorithms=[ALGORITHM])

    try:
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception

    async with Db.session() as session:
        db_user: User = await session.execute_read(user_get_tx, username=token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
