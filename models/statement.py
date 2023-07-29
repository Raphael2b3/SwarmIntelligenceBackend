from bson import ObjectId
from pydantic import BaseModel


class Statement:
    _id: str
    value: str


class StatementDB(BaseModel):
    _id: ObjectId
    value: str
