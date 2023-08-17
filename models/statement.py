from typing import Any

from bson import ObjectId
from pydantic import BaseModel

from models.connection import Connection


class Statement(BaseModel):
    id: str = None
    value: str = None

