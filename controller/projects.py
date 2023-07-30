from const import DB_COLLECTION_NAME_PROJECTS

from services import dbcontroller


def create(doc):
    return dbcontroller.create_document(document=doc, collection=DB_COLLECTION_NAME_PROJECTS)


def delete(doc):
    return dbcontroller.create_document(document=doc, collection=DB_COLLECTION_NAME_PROJECTS)


def get_many(doc):
    return dbcontroller.find_many_document(DB_COLLECTION_NAME_PROJECTS, doc)


def get_one(doc):
    return dbcontroller.find_document(DB_COLLECTION_NAME_PROJECTS, doc)
