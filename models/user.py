from bson import ObjectId
from pydantic import BaseModel


class Vote(BaseModel):
    object: int
    value: float | int = None


class CreateUserRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str = None
    hashed_password: str = None
    disabled: bool = None
