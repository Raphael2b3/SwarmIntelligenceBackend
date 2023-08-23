from pydantic import BaseModel


class User(BaseModel):
    username: str|None= None
    hashed_password: str |None= None
    disabled: bool |None= None
