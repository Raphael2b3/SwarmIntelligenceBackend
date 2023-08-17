from typing import Literal

from bson import ObjectId
from pydantic import BaseModel
from pymongo.results import InsertOneResult

from services.dbcontroller import driver
from models.report import Report
from models.user import User, Vote


def create(*, username, hashed_password):
    driver.execute_query("""
    MERGE (c:User{username:$username})
    WITH c 
    SET c.hashed_password = $hashed_password
    """, username=username, hashed_password=hashed_password)


def delete(username):
    driver.execute_query("""
        MATCH (c:User{username:$username})
        DELETE c""", username=username)


def get_hashed_password(username):
    records, _, __ = driver.execute_query("""
        MATCH (c:User{username:$username})
        RETURN c.hashed_password as hashedpassword
    """, username=username)
    try:
        return list(records)[0]["hashedpassword"]
    except Exception as e:
        print(e)
        return None


def modify_star(username, objectid, _type="Project|Statement|User", removestar=False):
    _type = _type.capitalize()
    if _type not in ["Project", "Statement", "User", "Project|Statement|User"]:
        raise Exception("Invalid Object of Label name " + _type)

    records, _, __ = driver.execute_query(f"""
            MATCH (u:User{{username:$username}})
            MATCH (o:{_type}{{id:$objectid}})
            CALL {{
                WITH *
                WITH * WHERE NOT $removestar
                MERGE (u)-[r:STARED]->(o)
            UNION
                WITH *
                WITH * WHERE $removestar
                OPTIONAL MATCH (u)-[r:STARED]->(o) 
                DELETE r
            }}
            
            
            
            """, username=username, removestar=removestar, objectid=objectid, )


def report(objectid, reason="", _type="Project|Statement|User", ):
    _type = _type.capitalize()
    if _type not in ["Project", "Statement", "User", "Project|Statement|User"]:
        raise Exception("Invalid Object of Label name " + _type)
    records, _, __ = driver.execute_query(f"""
            MATCH (o:{_type}{{id:$objectid}})
            OPTIONAL MATCH (o)<-[r:REPORTED]-(:Report)
            WITH r WHERE r is Null
            MERGE (o)<-[r:REPORTED{{message:$message}}]-(:Report)
            """, objectid=objectid, message=reason)


def get_user(username):
    records, _, __ = driver.execute_query("""
            MATCH (c:User{username:$username})
            RETURN c.disablet as disablet, c.username as username
        """, username=username)
    try:
        return User(**dict(records[0]))
    except Exception as e:
        print(e)
        return None
