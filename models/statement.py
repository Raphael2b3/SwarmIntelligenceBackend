from bson import ObjectId
from pydantic import BaseModel

class Statement(BaseModel):
    value: str = None
    upvotes: int = None
    downvotes: int = None
    misunderstood: int = None