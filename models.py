from pydantic import BaseModel


class ProjectRequest(BaseModel):
    _id: str
    q: str
    depth: int = 4
    width: int = 5
    sortmethod: str
    max: int = 5


class StatementRequest(BaseModel):
    _id: str
    q: str
    depth: int = 4
    width: int = 5
    sortmethod: str
    max: int = 5


class CreateUserRequest(BaseModel):
    username: str
    password: str
