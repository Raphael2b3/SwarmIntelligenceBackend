import pymongo
from pydantic import BaseModel
from pymongo import MongoClient
from pandas import DataFrame
from const import DB_CONNECTION_STRING, DB_NAME, DB_COLLECTION_NAME_CONNECTIONS, DB_COLLECTION_NAME_PROJECTS, \
    DB_COLLECTION_NAME_STATEMENTS, DB_COLLECTION_NAME_USERS


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(DB_CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client[DB_NAME]


db = get_database()

connectionsDB = db[DB_COLLECTION_NAME_CONNECTIONS]
connectionsDB.create_index([("hash", pymongo.ASCENDING)])

projectsDB = db[DB_COLLECTION_NAME_PROJECTS]
statementsDB = db[DB_COLLECTION_NAME_STATEMENTS]
usersDB = db[DB_COLLECTION_NAME_USERS]

