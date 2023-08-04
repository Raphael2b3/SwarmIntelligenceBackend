from pydantic import BaseModel, computed_field, ConfigDict, Field

from models.mongomodel import MongoModel, PydanticObjectId


# stm = statement


class Connection(MongoModel):
    stm_start: PydanticObjectId = None
    stm_stop: PydanticObjectId = None
    stm_type: str = None
    weight: float = None
    replies: int = None

    @computed_field
    @property
    def hash(self) -> str | None:
        return f"{self.stm_start}{self.stm_stop}" if self.stm_stop and self.stm_start else None
