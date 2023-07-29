from bson import ObjectId


class Project:
    _id: ObjectId
    name: str
    statements: list[int]
    connections: list[int]

