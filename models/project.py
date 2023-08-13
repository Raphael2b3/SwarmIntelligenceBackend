from bson import ObjectId
from pydantic import BaseModel



class Project(BaseModel):
    pass


class ProjectQuery(BaseModel):
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None
