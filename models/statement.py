from bson import ObjectId
from pydantic import BaseModel

from models.mongomodel import MongoModel


class Statement(MongoModel):
    value: str = None
