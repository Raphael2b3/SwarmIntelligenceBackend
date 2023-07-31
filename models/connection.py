from bson import ObjectId
from pydantic import BaseModel, computed_field, ConfigDict
from models.helper_definitions import CustomBaseModel

# stm = statement


class Connection(CustomBaseModel):
    _id: ObjectId
    projectId: ObjectId
    stm_start: ObjectId
    stm_stop: ObjectId
    stm_type: str
    weight: float

    @computed_field
    @property
    def hash(self)->str:
        return f"{self.stm_start}{self.stm_stop}"
