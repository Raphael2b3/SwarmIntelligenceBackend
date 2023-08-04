from const import DB_COLLECTION_NAME_USERS

from services.dbcontroller import usersDB


def create(doc):
    return usersDB.insert_one(document=doc)


def delete(doc):
    return usersDB.delete_one(document=doc)


def get_one(doc):
    return usersDB.find_one(doc)


def get_many(doc):
    return usersDB.find(doc)