from bson import ObjectId
from pydantic import BaseModel

from models.mongomodel import MongoModel, PydanticObjectId


class Project(MongoModel):
    name: str = None
    connections: list[PydanticObjectId]  = None
