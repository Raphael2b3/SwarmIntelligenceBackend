from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str


class CreateTagRequest(BaseModel):
    value: str


class CreateStatementRequest(BaseModel):
    value: str
    tags: list


class CreateConnectionRequest(BaseModel):
    parent_id: str
    child_id: str
    supports: bool


class VoteStatementRequest(BaseModel):
    id: str
    value: str


class VoteConnectionRequest(BaseModel):
    id: str
    value: bool


class CreateReportRequest(BaseModel):
    id: str
    value: str


class SetStarRequest(BaseModel):
    id: str
    value: bool


class SetTagRequest(BaseModel):
    id: str
    tags: list[str]


class DeleteRequest(BaseModel):
    id: str


class SearchStatementRequest(BaseModel):
    q: str
    tags: list[str]
    results: int
    skip: int
    # TODO add filter params


class SearchTagRequest(BaseModel):
    q: str
    results: int
    skip: int
    # TODO add filter params


class ContextRequest(BaseModel):
    id: str
    exclude_ids: list[str]
