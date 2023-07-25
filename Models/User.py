from pydantic import BaseModel

from Models.Statement import Statement


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    statements: list[Statement]


class UserInDB(User):
    hashed_password: str

