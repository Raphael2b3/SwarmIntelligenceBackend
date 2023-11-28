from uuid import uuid4

from db.core import transaction


@transaction
async def tag_create(tx, *, tag, username):
    r = await tx.run("""
    MATCH (u:User{username:$username})
    OPTIONAL MATCH (p:Tag{value:$tag})
    WITH p, u WHERE p IS NULL
    MERGE (u)-[:CREATED]->(:Tag{id:$id,value:$tag})
    RETURN 1
    """, tag=tag, username=username, id=str(uuid4()))
    success = await r.value()
    log = "tags created successfully" if success else "Error: Tag already exists"
    print(log)
    return {"message": log}


@transaction
async def tag_delete(tx, *, tag, username):
    r = await tx.run("""
        MATCH (p:Tag{id:$tag})<-[:CREATED]-(:User{username:$username})
        DETACH DELETE p
        RETURN 1
        """, tag=tag, username=username)
    success = await r.value()
    log = "tags deleted successfully" if success else "Error: Tag may not exist, you are not creator of statement"
    print(log)
    return Response(message=log)


@transaction
async def tag_get_many(tx, query_string, n_results=10, skip=0):
    print("tag get", query_string, n_results, skip)
    await tx.run("""
                CALL db.index.fulltext.awaitEventuallyConsistentIndexRefresh()
                """)
    result = await tx.run("""
            CALL{
                    CALL db.index.fulltext.queryNodes($index, $query_string,{
                        skip:$skip,
                        limit:$limit
                    }) YIELD node, score
                    return node.value as value, node.id as id
                UNION
                    MATCH (a:Tag)
                    WHERE a.value CONTAINS $query_string
                    RETURN a.value as value, a.id as id
                }
                RETURN DISTINCT *
            """, query_string=query_string, index=IndexesAndConstraints.tagsFullText, limit=n_results, skip=skip)
    log = "success"
    return Response(message=log, value=[dict(record) for record in await result.fetch(n_results)])
