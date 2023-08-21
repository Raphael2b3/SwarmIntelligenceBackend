from pydantic import BaseModel


class RequestUserCreate(BaseModel):
    username: str
    password: str


class RequestTagCreate(BaseModel):
    value: str


class RequestStatementCreate(BaseModel):
    value: str
    tags: list


class RequestConnectionCreate(BaseModel):
    parent_id: str
    child_id: str
    supports: bool


class RequestStatementVote(BaseModel):
    id: str
    value: str


class RequestConnectionVote(BaseModel):
    id: str
    value: bool


class RequestReportCreate(BaseModel):
    id: str
    value: str


class RequestStarSet(BaseModel):
    id: str
    value: bool


class RequestTagSet(BaseModel):
    id: str
    tags: list[str]


class RequestDelete(BaseModel):
    id: str


class RequestStatementSearch(BaseModel):
    q: str
    tags: list[str]
    results: int
    skip: int
    # TODO add filter params


class RequestTagSearch(BaseModel):
    q: str
    results: int
    skip: int
    # TODO add filter params


class RequestContext(BaseModel):
    id: str
    exclude_ids: list[str]
