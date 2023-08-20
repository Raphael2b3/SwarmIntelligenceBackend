from uuid import uuid4


async def project_create_tx(tx, *, projectname, username):
    await tx.run("""
    MATCH (u:User{username:$username})
    OPTIONAL MATCH (p:Project{value:$projectname})
    WITH p, u WHERE p IS NULL
    MERGE (u)-[:CREATED]->(:Project{id:$new_id,value:$projectname})
    
    """, projectname=projectname, username=username, new_id=str(uuid4()))


async def project_delete_tx(tx, *, projectname, username):
    await tx.run("""
        MATCH (p:Project{value:$projectname})<-[:CREATED]-(:User{username:$username})
        DETACHE DELETE p
        """, projectname=projectname, username=username)


async def project_get_many(tx, query_string, n_results=10):
    result = await tx.run("""
            MATCH (p:Project)
            WHERE p.value STARTS WITH $query_string
            RETURN p.value as value, p.id as id
            """, queryString=query_string)

    return [dict(record) async for record in await result.fetch(n_results)]
