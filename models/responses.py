from typing import Any

from pydantic import BaseModel


class ResponseConnection(BaseModel):
    id: str | None = None
    stm_parent_id: str | None = None
    stm_child_id: str | None = None
    supports: bool | None = None
    user_created: bool | None = None
    user_voted: int | None = None


class ResponseStatement(BaseModel):
    id: str | None = None
    truth: float | None = None
    arg_connection_ids: list | None = None
    parent_connection_ids: list | None = None
    tags: list | None = None
    user_created: bool | None = None
    user_voted: int | None = None


class ResponseTag(BaseModel):
    id: str | None = None
    value: str | None = None
    user_created: bool | None = None


class ResponseContext(BaseModel):
    statements: list[ResponseStatement] | None = None
    connections: list[ResponseConnection] | None = None


class DefaultResponse(BaseModel):
    message: str = ""
    value: Any = None
