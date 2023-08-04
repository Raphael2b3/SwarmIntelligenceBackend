from bson import ObjectId
from pydantic import BaseModel

from models.swarmintelligencemodel import SwarmIntelligenceModel, PydanticObjectId


class Project(SwarmIntelligenceModel):
    name: str = None
    rootstatements: list[PydanticObjectId] = None
    nstatements: int = None # TODO generateable
    nvotes: int = None  # TODO generateable


class ProjectQuery(BaseModel):
    filter: Project
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None
