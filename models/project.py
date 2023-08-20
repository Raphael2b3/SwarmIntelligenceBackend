from bson import ObjectId
from pydantic import BaseModel


class Project(BaseModel):
    id: str = None
    value: str = None


class ProjectQuery(BaseModel):
    q: str = ""
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None
