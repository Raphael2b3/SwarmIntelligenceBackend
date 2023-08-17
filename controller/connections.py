from uuid import uuid4

from neo4j import ResultSummary, Record
from pydantic import BaseModel

from models.user import User
from services.dbcontroller import driver
import models.connection

debugprefix = "Connection-Controller "


def create_connection(*, stopId, startId, supports, username):
    supportStr = "SUPPORTS" if supports else "OPPOSES"
    query = f"""
    MATCH (a:Statement{{id:$startId}}) 
    MATCH (b:Statement{{id:$stopId}})
    WITH a, b
    WHERE NOT (b)-[*]->(a) AND NOT (a)-[:HAS]->()-->(b)
    MERGE (a)-[:HAS]->(c:Connection{{id:$newId}})-[:{supportStr}]->(b)
    WITH c
    MATCH (u:User{{username:$username}})
    MERGE (u)-[:CREATED]->(c) 
    """

    records, summary, keys = driver.execute_query(query, startId=startId, stopId=stopId, supports=supportStr,
                                                  newId=str(uuid4()), username=username)
    print(*[record for record in list(records)])

def delete_connection(*, connectionId, username):
    print(debugprefix, "DeleteGlobally, ")
    query = """
            MATCH (c:Connection{id:$connectionId})
            MATCH (u:User{username:$username})
            WITH *
            WHERE (u)-[:CREATED]->(c) 
            DETACHE DELETE (c)
            """
    records, summary, keys = driver.execute_query(query, connectionId=connectionId, username=username)
    print(*[record for record in list(records)])


def weight_connection(*, connectionId, is_bad, username):
    query = """
        MATCH (c:Connection{id: $id})
        MATCH (u:User{username:$username})
        MERGE (u)-[r:WEIGHT]->(c)
        SET r.bad = $is_bad
        """

    records, summary, keys = driver.execute_query(query, id=connectionId, is_bad=is_bad, username=username)
    print(*[record for record in list(records)])
