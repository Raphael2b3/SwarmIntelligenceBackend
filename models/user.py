from bson import ObjectId
from pydantic import BaseModel

from models.helper_definitions import  CustomBaseModel


class User(CustomBaseModel):
    _id: ObjectId
    username: str
    hashed_password: str
    disabled: bool = False
