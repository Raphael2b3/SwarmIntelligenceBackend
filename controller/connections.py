from bson import ObjectId
from pydantic import BaseModel

from models.user import User
from services.dbcontroller import driver
import models.connection

debugprefix = "Connection-Controller "


class ConnectionQuery(BaseModel):
    filter: models.connection.Connection
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None


def create_connection(doc: models.connection.Connection, user: User):
    query = """
    MATCH (a:Statement), (b:Statement)
    WHERE b.id = $stopId AND a.id = $startId
    WITH a, b, NOT (b)-[*]->(a) AND NOT (a)-[*2]->(b) as A
    CALL {
        WITH *
        WITH * WHERE A
        MERGE (a)-[:connected_to]->(c:Connection)-[:$supports]->(b)
        return c as c
    }
    RETURN A, c
    """

    supportStr = "supports" if doc.supports else "opposes"
    result, c = driver.execute_query(query, startId=doc.stm_start, stopId=doc.stm_stop, supports=supportStr)
    print(result)
    if not result: raise "Couldnt create Connection"

    assign_author = """
        MATCH (c:$c) 
        MATCH (u:User{username:$username})
        MERGE (u)-[:created]->(c) 
    """
    result2 = driver.execute_query(assign_author, con=c, username=user.username)
    if not result2: raise "Couldnt asign author"
    print(result2)

def delete_connection(doc: models.connection.Connection, user: User):
    print(debugprefix, "DeleteGlobally", doc.model_dump())
    query = """
            MATCH (:Statement{id:{$startId})-->(c:Connection)-->(:Statement{id:{$stopId}), (u:User{username:$username})
            WHERE (u)-[:created]->(c) 
            DELETE (c)
            """
    result = driver.execute_query(query, startId=doc.stm_start, stopId=doc.stm_stop, username=user.username)
    print(result)


def weight_connection(connection: models.connection.Connection, user):
    query = """
        MATCH (:Statement{id:{$startId})-->(c:Connection)-->(:Statement{id:{$stopId}), (u:User{username:$username})
        WHERE NOT (u)-[:weight]->(c) 
        MERGE (u)-[:weight{weight:$weight}]->(c)
        """

    result = driver.execute_query(query, startId=connection.stm_start, stopId=connection.stm_stop,
                                  weight=connection.weight, username=user.username)
    print(result)
    if not result:
        raise "Couldnt create Connection"


def get_connection(doc: models.connection.Connection):
    pass
