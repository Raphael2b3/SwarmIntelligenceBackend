from bson import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    _id: str
    username: str
    password: str
    disabled: bool = False


class UserDB(BaseModel):
    _id: ObjectId
    username: str
    hashed_password: str
    disabled: bool = False
