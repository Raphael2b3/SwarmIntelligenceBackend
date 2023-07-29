from pydantic import BaseModel
from pymongo import MongoClient
from pandas import DataFrame
from const import DB_CONNECTION_STRING, DB_NAME

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(DB_CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client[DB_NAME]


db = get_database()


def create_document(collection, document: BaseModel):
    return db[collection].insert_one(document.model_dump())


def delete_document(collection, q: dict):
    return db[collection].delete_one(q)


def find_document(collection, q: dict):
    return db[collection].find_one(q)


def find_many_document(collection,q: dict = None, max_results=1, skip=0):
    return db[collection].find(q, limit=max_results, skip=skip)

