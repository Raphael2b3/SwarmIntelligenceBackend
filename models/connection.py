from pydantic import BaseModel, computed_field, ConfigDict, Field


# stm = statement


class Connection(BaseModel):
    id: str = None
    stm_start: int = None
    stm_stop: int = None
    supports: bool = None


