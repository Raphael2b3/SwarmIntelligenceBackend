import math
from uuid import uuid4

# ? Maby get user from db call bookmark before, because there will always be a validation for the  user before this call
from neo4j import ResultSummary

from db.dbcontroller import IndexesAndConstraints


async def statement_create_tx(tx, *, text, username, ):  #  TODO Inlcude Tags
    r = await tx.run("""
        MATCH (u:User{username:$username})
        OPTIONAL MATCH (p:Statement{value:$text})
        WITH p, u WHERE p IS NULL
        MERGE (u)-[:CREATED]->(:Statement{value:$text,id:$id})
        RETURN 1
        """, text=text, username=username, id=str(uuid4()))
    success = await r.value()
    return "statement created successfully" if success else "Error: statement already exist"


async def statement_delete_tx(tx, *, statement_id, username):
    r = await tx.run("""
            MATCH (p:Statement{id:$id})<-[:CREATED]-(:User{username:$username})
            WITH p
            DETACH DELETE p
            RETURN 1 
            """, id=statement_id, username=username)
    success = await r.value()
    return "statement deleted successfully" if success else "Error: statement may not exist, you are not creator of statement"


async def statement_get_many_tx(tx, *, query_string, n_results=10, skip=0):
    print("statement get", query_string, n_results, skip)
    await tx.run("""
                    CALL db.index.fulltext.awaitEventuallyConsistentIndexRefresh()
                    """)

    result = await tx.run("""
            CALL db.index.fulltext.queryNodes($index, $query_string,{
                skip:$skip,
                limit:$limit
            }) YIELD node, score
            return node.value as value, node.id as id
            """, query_string=query_string, limit=n_results, skip=skip, index=IndexesAndConstraints.statementsFullText)
    return [dict(record) for record in await result.fetch(n_results)]


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
    return "tags modified successfully" if success else "Error: statement may not exist, you are not creator of statement, tag may not exist"


async def statement_vote_tx(tx, *, username, statement_id, vote):
    r = await tx.run("""
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$id})
            MERGE (u)-[v:VOTED]->(s)
            SET v.value = $vote
            RETURN 1
    """, username=username, id=statement_id, vote=vote)
    success = await r.value()
    return "voted successfully" if success else "Error: statement may not exist, you are not creator of statement"


async def statement_get_context_tx(tx, *, statement_id):
    r = await tx.run("""
    
    """, id=statement_id)
    success = await r.value()
    success = True
    return "NOT YET IMPLEMENTED" if success else "Error: statement may not exist"
