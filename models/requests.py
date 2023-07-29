from pydantic import BaseModel


class SearchRequest:
    _id: str
    q: str
    depth: int = 4
    width: int = 5
    sort_method: str
    max: int = 5


class CreateUserRequest:
    username: str
    password: str
