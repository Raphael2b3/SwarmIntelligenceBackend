import json

from bson import ObjectId

from models.connection import Connection
from services.dbcontroller import connectionsDB

if __name__ == '__main__':
    p = Connection(id="0")
    print("default Connection Instance",p)

    d = p.model_dump()
    print("Dumped default Connection Instance", d)

    connectionsDB.insert_one(d)
    connectionWithId = connectionsDB.find_one(d)

    print("Connection dict from database",connectionWithId)

    s = Connection(**connectionWithId)
    print("Connection instance from dict from datatbase",s)

    a = s.model_dump()
    print("dumped instance from db",a)
    b = s.model_dump_json()
    print("json instance from db", b)

    connectionsDB.delete_one(a)
