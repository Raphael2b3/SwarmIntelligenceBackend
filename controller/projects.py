from pydantic import BaseModel

import models.project
from models.user import User

from services.dbcontroller import driver


def create(*, projectname, username):
    records, summary, keys = driver.execute_query("""
    MERGE (:Project{name:$projectname})
    """, projectname=projectname)

    if False: # get changed from summary
        raise Exception(f"Project {projectname} already exists")


def delete(*, projectname, username):
    records, summary, keys = driver.execute_query("""
        MATCH (p:Project{name:$projectname})<-[:CREATED]-(:User{username:$username})
        DETACHE DELETE p
        """, projectname=projectname, username=username)


def get_many(username, queryString):
    #TODO QUERY THRU queryString
    records, summary, keys = driver.execute_query("""
            MATCH (p:Project{name:$projectname})<-[:CREATED]-(:User{username:$username})
            DETACHE DELETE p
            """, queryString=queryString, username=username)

    return

