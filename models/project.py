from bson import ObjectId

from models.helper_definitions import CustomBaseModel


class Project(CustomBaseModel):
    _id: ObjectId
    name: str
    statements: list[ObjectId]
    connections: list[ObjectId]
