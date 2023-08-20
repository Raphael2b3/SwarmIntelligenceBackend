from pydantic import BaseModel, computed_field, ConfigDict, Field


#   TODO create good Schemes



class Connection(BaseModel):
    id: str = None
    stm_start: int = None
    stm_stop: int = None
    supports: bool = None
    is_bad: bool = None

