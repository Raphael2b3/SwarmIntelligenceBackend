from bson import ObjectId

from models.connection import Connection
from services.dbcontroller import connectionsDB

if __name__ == '__main__':
    #ObjectId("000000000000000000000000")
    connectionsDB.insert_one(Connection(stm_start="000000000000000000000000").model_dump())
