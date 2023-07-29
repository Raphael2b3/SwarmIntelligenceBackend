from bson import ObjectId
from pydantic import BaseModel


# stm = statement

class Connection:
    _id: str
    stm_start: int
    stm_stop: int
    stm_type: chr
    weight: float


class ConnectionDB:
    _id: ObjectId
    stm_start: ObjectId
    stm_stop: ObjectId
    stm_type: chr
    weight: float
