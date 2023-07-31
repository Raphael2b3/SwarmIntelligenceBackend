from bson import ObjectId
import models.connection
from services.dbcontroller import projectsDB, connectionsDB


def create(doc: models.connection.Connection):
    """
    Connection erstellen:

    1. Gucken ob das Projekt existiert
    2. gucken ob die Connection schon existiert
        - durch indexing in mongodb gehändelt
    3. connection hinzufügen
    :param doc:
    :return:
    """
    # 1.
    project = projectsDB.find_one({"_id": ObjectId(doc.projectId)})
    if not project: raise Exception("Project doesnt exists")
    connectionInstanceDB = models.connection.ConnectionDB(instance=doc)

    res = connectionsDB.insert_one(connectionInstanceDB.to_dict())
    connectionsDB.find_one({doc.model_dump()})
    return


def delete(doc):
    return dbcontroller.create_document(document=doc, collection=DB_COLLECTION_NAME_PROJECTS)


def get_many(doc):
    return dbcontroller.find_many_document(DB_COLLECTION_NAME_PROJECTS, doc)


def get_one(doc):
    return dbcontroller.find_document(DB_COLLECTION_NAME_PROJECTS, doc)
