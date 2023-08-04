from bson import ObjectId
from pydantic import BaseModel

from models.swarmintelligencemodel import SwarmIntelligenceModel


class Statement(SwarmIntelligenceModel):
    value: str = None
    upvotes: int = None
    downvotes: int = None
    misunderstood: int = None