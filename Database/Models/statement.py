from bson import ObjectId
from pydantic import BaseModel


class Statement(BaseModel):
    _id: ObjectId
    value: str