from bson import ObjectId
from pydantic import BaseModel
from pymongo.results import InsertOneResult
from const import DB_COLLECTION_NAME_USERS
from models.report import Report
from models.swarmintelligencemodel import SwarmIntelligenceModel
from models.user import User, Vote
from routes.users import CreateUserRequest

from services.dbcontroller import usersDB, reportDB, statementsDB, projectsDB
from services.jwt_auth import get_password_hash


def create(doc: CreateUserRequest):
    print("Create User:", doc.model_dump())
    user_in_db = User(name=doc.name, hashed_password=get_password_hash(doc.password))
    result = usersDB.insert_one(user_in_db.model_dump())
    return str(result)


def delete(doc: User):
    return usersDB.delete_one(doc.model_dump()).__str__()


dbmap = {
    "statement": statementsDB,
    "project": projectsDB,
    "user": usersDB
}


def modify_star(doc: User, object: SwarmIntelligenceModel, type, removestar=False):
    update = {"$addToSet": {"givenstars": object.id}} if not removestar else {"$pull": {"givenstars": object.id}}
    result = usersDB.update_one(doc.model_dump(), update)
    if result.modified_count:
        return dbmap[type].find_one_and_update(object.model_dump(), {"$inc": {"stars": -1 if removestar else 1}})
    return result


def report(object: Report, db):
    result = dbmap[db].update_one({"_id": object.objectId}, {"reported": True})
    if result.modified_count == 1:
        return reportDB.insert_one(object.model_dump())
