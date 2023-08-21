from pydantic import BaseModel



class ResponseConnection(BaseModel):
    id: str = None
    stm_parent_id: str = None
    stm_child_id: str = None
    supports: bool = None
    user_created: bool = None
    user_voted: int = None


class ResponseStatement(BaseModel):
    id: str = None
    truth: float = None
    arg_connection_ids: list = None
    parent_connection_ids: list = None
    tags: list = None
    user_created: bool = None
    user_voted: int = None


class ResponseTag(BaseModel):
    id: str = None
    value: str = None
    user_created: bool = None


class ResponseContext(BaseModel):
    statements: list[ResponseStatement]
    connections: list[ResponseConnection]
