from pydantic import BaseModel, computed_field, ConfigDict, Field


#   TODO create good Schemes

class ConnectionResponse(BaseModel):
    id: str = None
    stm_parent_id: str = None
    stm_child_id: str = None
    supports: bool = None
    user_created: bool = None
    user_voted: int = None


class StatementResponse(BaseModel):
    id: str = None
    truth: float = None
    arg_connection_ids: list = None
    parent_connection_ids: list = None
    tags: list = None
    user_created: bool = None
    user_voted: int = None


class TagResponse(BaseModel):
    id: str = None
    value: str = None
    user_created: bool = None


class ContextResponse(BaseModel):
    statements: list[StatementResponse]
    connections: list[ConnectionResponse]
