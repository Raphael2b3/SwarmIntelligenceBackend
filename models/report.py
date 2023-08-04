from pydantic import BaseModel

from models.swarmintelligencemodel import PydanticObjectId


class Report(BaseModel):
    message: str
    objectId: PydanticObjectId

