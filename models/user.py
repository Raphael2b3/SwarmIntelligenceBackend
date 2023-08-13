from bson import ObjectId
from pydantic import BaseModel


class Vote(BaseModel):
    object: int
    value: float | int = None


class CreateUserRequest(BaseModel):
    name: str
    password: str


class User(BaseModel):
    username: str = None
    hashed_password: str = None
    disabled: bool = None
    votes: list[Vote] = []
    givenstars: list[int] = []
