from pydantic import BaseModel, computed_field, ConfigDict, Field


# stm = statement


class Connection(BaseModel):
    stm_start: int = None
    stm_stop: int = None
    supports: bool = None
    weight: float = None


