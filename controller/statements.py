import models.requests as requests
from pydantic import BaseModel

import models.statement
from const import DB_COLLECTION_NAME_STATEMENTS

from services.dbcontroller import statementsDB


def create(doc: models.statement.Statement):
    stm = statementsDB.insert_one(doc.model_dump())

    return stm


def delete(doc: models.statement.Statement):
    return statementsDB.delete_one(doc.model_dump())


class StatementQuery(BaseModel):
    filter: models.statement.Statement
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None


def get_many(doc: StatementQuery):
    return statementsDB.find(**doc.model_dump())


def get_one(doc: models.statement.Statement):
    return statementsDB.find_one(doc.model_dump())
