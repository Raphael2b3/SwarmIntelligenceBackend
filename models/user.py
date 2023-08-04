from bson import ObjectId
from pydantic import BaseModel

from models.mongomodel import MongoModel


class User(MongoModel):
    username: str = None
    hashed_password: str = None
    disabled: bool = None
