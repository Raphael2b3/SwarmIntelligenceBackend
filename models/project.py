from bson import ObjectId
from pydantic import BaseModel


class ProjectDB:
    _id: ObjectId
    name: str
    statements: list[ObjectId]
    connections: list[ObjectId]


class Project:
    _id: str
    name: str
    statements: list[str]
    connections: list[str]
