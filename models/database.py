from pydantic import BaseModel


class User(BaseModel):
    username: str = None
    hashed_password: str = None
    disabled: bool = None

