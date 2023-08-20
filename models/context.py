from pydantic import BaseModel


class StatementContext(BaseModel):
    id: str = None
    value: str = None
    w: float = None
    args: list["ConnectionContext"]
    parents: list["ConnectionContext"]
    tags: list[str]
    user_vote: int = 0  # 1: upvote, 0: Neutral, -1: down
    user_is_author: bool = None  # 1: upvote, 0: Neutral, -1: down


class ConnectionContext(BaseModel):
    id: str = None
    supports: bool = None
    statement: StatementContext
    user_disapprove: bool = False
    user_is_author: bool = None


class StatementContext(BaseModel):
    id: str = None
    value: str = None
    w: float = None
    args: list["ConnectionContext"]
    parents: list["ConnectionContext"]
    tags: list[str]
    user_vote: int = 0  # 1: upvote, 0: Neutral, -1: down
    user_is_author: bool = None  # 1: upvote, 0: Neutral, -1: down


class ContextRequest(BaseModel):
    id: str = None,

    parentgenerations: int = 1,
    n_parents: int = 3,
    skip_parents: int = 0,

    childgenerations: int = 2,
    n_childs: int = 6,
    skip_childs: int = 0
