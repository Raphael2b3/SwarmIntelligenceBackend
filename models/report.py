from pydantic import BaseModel



class Report(BaseModel):
    message: str
    objectId: int

