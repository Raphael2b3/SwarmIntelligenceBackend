from .requests import *
from .responses import *


class User(BaseModel):
    username: str
    hashed_password: str
