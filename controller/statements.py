from pydantic import BaseModel

import models.statement



def create(doc: models.statement.Statement):
    pass


def delete(doc: models.statement.Statement):
    return

class StatementQuery(BaseModel):
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None


def get_many(doc: StatementQuery):
    return

def get_one(doc: models.statement.Statement):
    return