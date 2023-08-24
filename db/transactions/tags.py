from uuid import uuid4

from neo4j import ResultSummary

from db.dbcontroller import IndexesAndConstraints


async def tag_create_tx(tx, *, tag, username):
    r = await tx.run("""
    MATCH (u:User{username:$username})
    OPTIONAL MATCH (p:Tag{value:$tag})
    WITH p, u WHERE p IS NULL
    MERGE (u)-[:CREATED]->(:Tag{id:$id,value:$tag})
    RETURN 1
    """, tag=tag, username=username, id=str(uuid4()))
    success = await r.value()
    return "tags created successfully" if success else "Error: Tag already exists"


async def tag_delete_tx(tx, *, tag, username):
    r = await tx.run("""
        MATCH (p:Tag{id:$tag})<-[:CREATED]-(:User{username:$username})
        DETACH DELETE p
        RETURN 1
        """, tag=tag, username=username)
    success = await r.value()
    return "tags deleted successfully" if success else "Error: Tag may not exist, you are not creator of statement"


async def tag_get_many_tx(tx, query_string, n_results=10,skip=0):
    result = await tx.run("""
            CALL db.index.fulltext.queryNodes($index, $query_string,{
                skip:$skip,
                limit:$limit
            }) YIELD node, score
            return node.value as value, node.id as id
            """, query_string=query_string,index=IndexesAndConstraints.statementsFullText,limit=n_results,skip=skip)

    return [dict(record) for record in await result.fetch(n_results)]
