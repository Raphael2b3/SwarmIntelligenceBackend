from bson import ObjectId
from pydantic import BaseModel
from pymongo.results import InsertOneResult

import services.dbcontroller
from models.report import Report
from models.user import User, Vote
from models.user import CreateUserRequest


def create(doc: CreateUserRequest):
    print("Create User:", doc.model_dump())
    return


def delete(doc: User):
    return


def get_hashed_password(doc: User):
    query = """
        MATCH (c:User{username:$username})
        RETURN c.hashed_password
    """
    return services.dbcontroller.driver.execute_query(query, username=doc.username)


def modify_star(user: User, type, removestar=False):
    query = """
    MATCH (u:User{username:$username}), (o:$label{id:$id})
    WITH (u)-[:stared]->(o) AND $removestar as remove
    CALL {
        WITH *
        WITH * WHERE remove
        MATCH ()
        UNION
    }
         
    """
    return


def report(object: Report, db):
    pass
