from pydantic import BaseModel


class RequestUserCreate(BaseModel):
    username: str | None = None
    password: str | None = None


class RequestTagCreate(BaseModel):
    value: str | None = None


class RequestStatementCreate(BaseModel):
    value: str | None = None
    tags: list | None = None


class RequestConnectionCreate(BaseModel):
    parent_id: str | None = None
    child_id: str | None = None
    supports: bool | None = None


class RequestUserPasswordChange(BaseModel):
    old: str | None = None
    new: str | None = None


class RequestStatementVote(BaseModel):
    id: str | None = None
    value: str | int | None = None


class RequestConnectionVote(BaseModel):
    id: str | None = None
    value: bool | float | None = None


class RequestReportCreate(BaseModel):
    id: str | None = None
    value: str | None = None


class RequestStarSet(BaseModel):
    id: str | None = None
    value: bool | None = None


class RequestTagSet(BaseModel):
    id: str | None = None
    tags: list[str] | None = None


class RequestStatementSearch(BaseModel):
    q: str | None = None
    tags: list[str] | None = None
    results: int = 10
    skip: int | None = None


class RequestTagSearch(BaseModel):
    q: str | None = None
    results: int = 10
    skip: int | None = None


class RequestContext(BaseModel):
    id: str | None = None
    exclude_ids: list[str] | None = None
