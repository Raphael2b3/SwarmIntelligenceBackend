from uuid import uuid4

from neo4j import ResultSummary


async def tag_create_tx(tx, *, tag, username):
    r = await tx.run("""
    PROFILE
    MATCH (u:User{username:$username})
    OPTIONAL MATCH (p:Tag{value:$tag})
    WITH p, u WHERE p IS NULL
    MERGE (u)-[:CREATED]->(:Tag{id:$id,value:$tag})
    
    """, tag=tag, username=username, id=str(uuid4()))
    summary: ResultSummary = await r.consume()
    return summary.profile


async def tag_delete_tx(tx, *, tag, username):
    r = await tx.run("""
        PROFILE
        MATCH (p:Tag{id:$tag})<-[:CREATED]-(:User{username:$username})
        DETACH DELETE p
        """, tag=tag, username=username)
    summary: ResultSummary = await r.consume()
    return summary.profile


async def tag_get_many_tx(tx, query_string, n_results=10):  # TODO Limit result on n_results
    result = await tx.run("""
            PROFILE
            MATCH (p:Tag)
            WHERE p.value STARTS WITH $query_string
            RETURN p.value as value, p.id as id
            """, query_string=query_string)

    return [dict(record) for record in await result.fetch(n_results)]
