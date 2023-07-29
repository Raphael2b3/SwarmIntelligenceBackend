from bson import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    _id: ObjectId
    username: str
    hashed_password: str
    disabled: bool = False
