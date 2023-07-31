from bson import ObjectId
from pydantic import BaseModel

from models.helper_definitions import  CustomBaseModel


class Statement(CustomBaseModel):
    _id: ObjectId
    value: str
