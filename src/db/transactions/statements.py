import math

from uuid import uuid4

# ? Maby get user from db call bookmark before, because there will always be a validation for the  user before this call
from neo4j import ResultSummary, AsyncResult

from db.dbcontroller import IndexesAndConstraints
from models.responses import Response, Statement

from builtins import print as _print

def print(*args, **kwargs):
    _print("TX: ", *args, "\n", **kwargs)


async def statement_create_tx(tx, *, text, username, tags=()):  # TODO Inlcude Tags
    r: AsyncResult = await tx.run("""
        OPTIONAL MATCH (s:Statement{value:$text})
        CALL{
            WITH s
            WITH s
            WHERE s IS NOT NULL
            RETURN s.id as id,  FALSE as user_created
        UNION
            WITH s
            WITH s 
            WHERE s IS NULL
            MATCH (u:User{username:$username})
            CREATE (u)-[:CREATED]->(:Statement{value:$text,id: $new_id})
            RETURN $new_id as id, TRUE as user_created
            }
        RETURN DISTINCT *
        """, text=text, username=username, new_id=str(uuid4()))

    success = await r.single()
    log = "statement created successfully" if success[
        "user_created"] else "Error: statement may not exist, connection already exists or argument cicle"
    print(log)
    return Response(message=log, value=Statement(**dict(success), value=text))


async def statement_delete_tx(tx, *, statement_id, username):
    r = await tx.run("""
            MATCH (p:Statement{id:$id})<-[:CREATED]-(:User{username:$username})
            WITH p
            DETACH DELETE p
            RETURN 1 
            """, id=statement_id, username=username)
    success = await r.value()
    log = "statement deleted successfully" if success else "Error: statement may not exist, you are not creator of statement"
    print(log)
    return Response(message=log)


async def statement_get_many_tx(tx, *, query_string, n_results=10, skip=0):
    print("statement get", query_string, n_results, skip)
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
                    MATCH (a:Statement)
                    WHERE a.value CONTAINS $query_string
                    RETURN a.value as value, a.id as id
                }
                RETURN DISTINCT *
            
            """, query_string=query_string, limit=n_results, skip=skip, index=IndexesAndConstraints.statementsFullText)
    log = "success"
    return Response(message=log, value=[dict(record) for record in await result.fetch(n_results)])


async def statement_modify_tag_tx(tx, *, username, statement_id, tags):
    print("Modify tag", username, statement_id, tags)
    r = await tx.run("""
            MATCH (:User{username:$username})-[:CREATED]->(s:Statement{id:$id})
            OPTIONAL MATCH (s)-[r:TAGGED]->(t:Tag)
            WITH s,t, collect(t) as ts, collect(r) as rs
            WITH rs,ts,s,t, range(0,size(ts)-1) as indexes, $tags as new_tags
            CALL{
                WITH rs,ts,indexes,new_tags
                UNWIND indexes as i
                WITH rs,ts,i,new_tags
                WHERE NOT ts[i].value IN new_tags
                DELETE rs[i]
            }
            CALL{
            WITH t,s, new_tags
            WITH s, new_tags, collect(t.value) as old
            UNWIND new_tags as tag
                WITH s,tag,old
                WHERE NOT tag IN old
                MATCH (q:Tag{value:tag})
                CREATE (s)-[:Tagged]->(q)
            }
            RETURN 1
    """, username=username, id=statement_id, tags=tags)
    success = await r.value()
    log = "tags modified successfully" if success else "Error: statement may not exist, you are not creator of statement, tag may not exist"
    print(log)
    return Response(message=log)


async def statement_vote_tx(tx, *, username, statement_id, vote):
    r = await tx.run("""
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$id})
            MERGE (u)-[v:VOTED]->(s)
            SET v.value = $vote
            RETURN 1
    """, username=username, id=statement_id, vote=vote)
    success = await r.value()
    log = "voted successfully" if success else "Error: statement may not exist, you are not creator of statement"
    print(log)
    return Response(message=log)


async def statement_get_context_tx(tx, *, statement_id, exclude_ids):  # TODO make get context work with exclude_ids
    return Response(message="NOT YET IMPLEMENTED")
    r = await tx.run("""
    
    """, id=statement_id)
    success = await r.value()
    success = True
    log = "NOT YET IMPLEMENTED" if success else "Error: statement may not exist"
    print(log)
    return Response(message=log)
