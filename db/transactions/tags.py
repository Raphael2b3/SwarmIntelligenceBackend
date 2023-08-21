from uuid import uuid4


async def tag_create_tx(tx, *, tag, username):
    await tx.run("""
    MATCH (u:User{username:$username})
    OPTIONAL MATCH (p:Tag{value:$tag})
    WITH p, u WHERE p IS NULL
    MERGE (u)-[:CREATED]->(:Tag{id:$id,value:$tag})
    
    """, tag=tag, username=username, id=str(uuid4()))


async def tag_delete_tx(tx, *, tag, username):
    await tx.run("""
        MATCH (p:Tag{value:$tag})<-[:CREATED]-(:User{username:$username})
        DETACHE DELETE p
        """, tag=tag, username=username)


async def tag_get_many_tx(tx, query_string, n_results=10): # TODO Limit result on n_results
    result = await tx.run("""
            MATCH (p:Tag)
            WHERE p.value STARTS WITH $query_string
            RETURN p.value as value, p.id as id
            """, query_string=query_string)

    return [dict(record) for record in await result.fetch(n_results)]
