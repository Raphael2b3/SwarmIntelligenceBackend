from pydantic import BaseModel

from models.project import Project

from services.dbcontroller import driver


def create(*, projectname, username):
    records, summary, keys = driver.execute_query("""
    MATCH (u:User{username:$username})
    OPTIONAL MATCH (p:Project{name:$projectname})
    WITH p, u WHERE p is null
    MERGE (:Project{name:$projectname})<-[:CREATED]-(u)
    
    """, projectname=projectname, username=username)

    if False:  # get changed from summary
        raise Exception(f"Project {projectname} already exists")


def delete(*, projectname, username):
    records, summary, keys = driver.execute_query("""
        MATCH (p:Project{name:$projectname})<-[:CREATED]-(:User{username:$username})
        DETACHE DELETE p
        """, projectname=projectname, username=username)


def get_many(queryString):
    # TODO make good query
    records, summary, keys = driver.execute_query("""
            MATCH (p:Project)
            WHERE p.name STARTS WITH $queryString
            return p.name as name, p.id as id
            """, queryString=queryString)
    return [dict(record) for record in records]
