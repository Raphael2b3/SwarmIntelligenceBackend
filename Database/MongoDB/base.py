from pymongo import MongoClient
from pandas import DataFrame


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['swarmintelligence']


dbname = get_database()
user_collection = dbname["user"]
project_collection = dbname["project"]
statement_collection = dbname["statement"]
