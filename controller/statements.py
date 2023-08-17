from pydantic import BaseModel

from models.statement import Statement

from services.dbcontroller import driver


def create(*, text, username, ):
    records, summary, keys = driver.execute_query("""
        MATCH (u:User{username:$username})
        OPTIONAL MATCH (p:Statement{text:$text})
        WITH p, u WHERE p is null
        MERGE (:Statement{text:$text})<-[:CREATED]-(u)
        """, text=text, username=username)


def delete(statementId, username):
    records, summary, keys = driver.execute_query("""
            MATCH (p:Statement{id:$statementId})<-[:CREATED]-(:User{username:$username})
            DETACHE DELETE p
            """, statementId=statementId, username=username)


def get_many(queryString):
    records, summary, keys = driver.execute_query("""
            MATCH (p:Statement)
            WHERE p.name STARTS WITH $queryString
            return p
            """, queryString=queryString)

    return [Statement(**dict(record)) for record in records]


def get_context(statementId, username, parentgenerations=1, childgeneration=1):
    records, summary, keys = driver.execute_query("""
                MATCH (u:User{username:$username})
                MATCH (p:Statement{id:$statementId})#
                WITH u,p
                
                return p
                """, queryString=queryString)

    return [Statement(**dict(record)) for record in records]


def calc_w2():
    q = """
    MATCH (p:Statement)
    WHERE NOT (p)<--(:Connection)
    WITH p
    MATCH (p)-[:HAS]->(:Connection)-->(i:Statement)
    WITH *
    
    """