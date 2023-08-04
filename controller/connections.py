from bson import ObjectId
from pydantic import BaseModel

import models.connection

from models.swarmintelligencemodel import SwarmIntelligenceModel
from services.dbcontroller import projectsDB, connectionsDB

debugprefix = "Connection-Controller "


def create(doc: models.connection.Connection):
    print(debugprefix, "Create", doc.model_dump())
    result = connectionsDB.insert_one(doc.model_dump())
    print(result)
    return result


def delete_globally(doc: models.connection.Connection):
    print(debugprefix, "DeleteGlobally", doc.model_dump())
    projectsDB.update_many({"connections": {"$contains": doc.id}}, {"connections":{"$pull":doc.id}})  # TODO
    return


class ConnectionQuery(BaseModel):
    filter: models.connection.Connection
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None


def get_many(doc: ConnectionQuery):
    """ # TODO Find every connection that match the filter: doc

    :param doc:
    :return:
    """
    return connectionsDB.find(*doc.model_dump(exclude_none=True))


def get_one(doc: models.connection.Connection):
    return connectionsDB.find_one(doc.model_dump())
