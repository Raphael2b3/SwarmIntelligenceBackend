from pydantic import BaseModel

from models.statement import Statement

from services.dbcontroller import driver


def create(*, text, username, ):
    records, summary, keys = driver.execute_query("""
        MATCH (u:User{username:$username})
        OPTIONAL MATCH (p:Statement{value:$text})
        WITH p, u WHERE p is null
        MERGE (:Statement{value:$text})<-[:CREATED]-(u)
        """, text=text, username=username)


def delete(statementId, username):
    records, summary, keys = driver.execute_query("""
            MATCH (p:Statement{id:$statementId})<-[:CREATED]-(:User{username:$username})
            DETACHE DELETE p
            """, statementId=statementId, username=username)


def get_many(queryString, username: str | None):  # username can be None! TODO Do it right with user context
    records, summary, keys = driver.execute_query("""
            MATCH (p:Statement)
            WHERE p.value STARTS WITH $queryString
            return p.value as value, p.id as id
            """, queryString=queryString)

    return [dict(record) for record in records]


def calc_w():
    q = """
    MATCH (p:Statement)
    WHERE NOT (p)<--(:Connection)
    WITH p
    MATCH (p)-[:HAS]->(:Connection)-->(i:Statement)
    WITH *
    
    """


def get_context(statementId, username, parentgenerations=1, n_parents=3, skip_parents=0, childgenerations=1,
                n_children=8, skip_children=0, ):  # TODO GOTTLOS VALLAH JA
    records, summary, keys = driver.execute_query("""
                MATCH (u:User{username:$username})
                MATCH (p:Statement{id:$statementId})#
                WITH u,p
                
                return p
                """, queryString=queryString)

    return [Statement(**dict(record)) for record in records]
