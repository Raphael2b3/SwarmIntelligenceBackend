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


# TODO Document the API with sample output and sample Input