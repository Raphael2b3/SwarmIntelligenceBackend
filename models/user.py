from bson import ObjectId
from pydantic import BaseModel

from models.swarmintelligencemodel import SwarmIntelligenceModel, PydanticObjectId


class Vote(BaseModel):
    object: PydanticObjectId
    value: float | int = None


class CreateUserRequest(BaseModel):
    name: str
    password: str


class User(SwarmIntelligenceModel):
    username: str = None
    hashed_password: str = None
    disabled: bool = None
    votes: list[Vote] = []
    givenstars: list[PydanticObjectId] = []
