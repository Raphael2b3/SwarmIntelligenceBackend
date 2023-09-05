from typing import Any, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    message: str = ""
    value: T | None = None


class Connection(BaseModel):
    id: str | None = None
    stm_parent_id: str | None = None
    stm_child_id: str | None = None
    supports: bool | None = None
    user_created: bool | None = None
    user_voted: int | None = None


class Statement(BaseModel):
    id: str | None = None
    value: str | None = None
    truth: float | None = None
    arg_connection_ids: list | None = None
    parent_connection_ids: list | None = None
    tags: list | None = None
    user_created: bool | None = None
    user_voted: int | None = None


class Tag(BaseModel):
    id: str | None = None
    value: str | None = None
    user_created: bool | None = None


class Context(BaseModel):
    statements: list[Statement] | None = None
    connections: list[Connection] | None = None
