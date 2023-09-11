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


async def statement_get_context_tx(tx, *, statement_id, exclude_ids,
                                   username):  # TODO make get context work with exclude_ids
    # TODO make it to Customfunction jar
    # return Response(message="NOT YET IMPLEMENTED")
    r = await tx.run("""
        MATCH (a:Statement) WHERE a.id = "9a3bb07a-571c-4b79-8888-9388641534bb"
        OPTIONAL MATCH (u:User) WHERE u.username="1"
        
        /// ROOT 
            
        // statement

        OPTIONAL MATCH (a)<-[:SUPPORTS|OPPOSES]-(cArg:Connection)
        
        WITH a, u, collect(cArg.id) as cArgs
        
        OPTIONAL MATCH (a)-[:HAS]->(cParent:Connection)
        
        WITH a, u, cArgs, collect(cParent.id) as cParents
        
        OPTIONAL MATCH (a)-[:TAGGED]->(t:Tag)
        WITH a, u, cArgs, cParents, collect(t.value) as tags
        OPTIONAL MATCH (u)-[uc:CREATED]->(a)
        OPTIONAL MATCH (u)-[r:VOTED]->(a)
        
        WITH a, u, uc, r, cArgs, cParents, tags, collect({ // maby less is allowed
                    id:a.id, 
                    value:a.value,
                    truth:a.truth,
                    arg_connection_ids:cArgs,
                    parent_connection_ids:cParents,
                    tags:tags,
                    user_created:uc IS NOT NULL,
                    user_voted:r.value
                }) as root_stm
        


        // arg_connection

        WITH a, u, root_stm
        OPTIONAL MATCH (a)<-[argSup:SUPPORTS|OPPOSES]-(cArg:Connection)<-[:HAS]-(sArg:Statement)
        OPTIONAL MATCH (u)-[uc2:CREATED]->(cArg)
        OPTIONAL MATCH (u)-[r2:VOTED]->(cArg)
        
        WITH a, u, root_stm, collect({
            id:cArg.id, 
            stm_parent_id:a.id,
            stm_child_id:sArg.id,
            supports:TYPE(argSup) = "SUPPORTS",
            user_created:uc2 IS NOT NULL,
            user_voted:r2.value
        }) as arg_connections

        
        
        // parent_connection

        WITH a, u, root_stm, arg_connections
        OPTIONAL MATCH (a)-[:HAS]->(cParent:Connection)-[parentSup:SUPPORTS|OPPOSES]->(sParent:Statement)
        OPTIONAL MATCH (u)-[uc3:CREATED]->(cParent)
        OPTIONAL MATCH (u)-[r3:VOTED]->(cParent)
        
        WITH a, u, root_stm, arg_connections ,arg_connections + collect({
            id:cParent.id, 
            stm_parent_id:sParent.id,
            stm_child_id:a.id,
            supports:TYPE(parentSup) = "SUPPORTS",
            user_created:uc3 IS NOT NULL,
            user_voted:r3.value
        }) as root_connections

        
        
        
        /// ARGS

        OPTIONAL MATCH (a)<-[:SUPPORTS|OPPOSES]-(:Connection)<-[:HAS]-(sArg:Statement)
        WITH sArg, a, u, root_connections, root_stm

        // statement

        OPTIONAL MATCH (sArg)<-[:SUPPORTS|OPPOSES]-(cArg:Connection)
        
        WITH sArg, u, collect(cArg.id) as cArgs, root_connections, root_stm, a
        
        OPTIONAL MATCH (sArg)-[:HAS]->(cParent:Connection)
        
        WITH sArg, u, cArgs, collect(cParent.id) as cParents, root_connections, root_stm, a
        
        OPTIONAL MATCH (sArg)-[:TAGGED]->(t:Tag)
        WITH sArg, u, cArgs, cParents, collect(t.value) as tags, root_connections, root_stm, a

        OPTIONAL MATCH (u)-[uc:CREATED]->(sArg)
        OPTIONAL MATCH (u)-[r:VOTED]->(sArg)
        
        WITH sArg, u, uc, r, cArgs, cParents, root_stm, tags,apoc.coll.union(
            collect({ 
                    id:sArg.id, 
                    value:sArg.value,
                    truth:sArg.truth,
                    arg_connection_ids:cArgs,
                    parent_connection_ids:cParents,
                    tags:tags,
                    user_created:uc IS NOT NULL,
                    user_voted:r.value
                }), root_stm) as ARG_stm, root_connections, a


        // arg_connections

        WITH sArg, u, ARG_stm, root_connections, a
        OPTIONAL MATCH (sArg)<-[argSup:SUPPORTS|OPPOSES]-(cArg:Connection)<-[:HAS]-(sArg2:Statement)
        OPTIONAL MATCH (u)-[uc2:CREATED]->(cArg)
        OPTIONAL MATCH (u)-[r2:VOTED]->(cArg)
        
        WITH sArg, u, ARG_stm,root_connections, apoc.coll.union(collect({
            id:cArg.id, 
            stm_parent_id:sArg.id,
            stm_child_id:sArg2.id,
            supports:TYPE(argSup) = "SUPPORTS",
            user_created:uc2 IS NOT NULL,
            user_voted:r2.value
        }),root_connections) as arg_connections, a

        
        
        // parent_connections

        WITH sArg, u, ARG_stm, arg_connections, a
        OPTIONAL MATCH (sArg)-[:HAS]->(cParent:Connection)-[parentSup:SUPPORTS|OPPOSES]->(sParent:Statement)
        OPTIONAL MATCH (u)-[uc3:CREATED]->(cParent)
        OPTIONAL MATCH (u)-[r3:VOTED]->(cParent)
        
        WITH sArg, u, ARG_stm,arg_connections, apoc.coll.union(arg_connections, collect({
            id:cParent.id, 
            stm_parent_id:sParent.id,
            stm_child_id:sArg.id,
            supports:TYPE(parentSup) = "SUPPORTS",
            user_created:uc3 IS NOT NULL,
            user_voted:r3.value
        })) as ARG_connections, a

        

        /// PARENTS
            

        WITH a, u, ARG_stm, ARG_connections
        OPTIONAL MATCH (a)-[:HAS]->(:Connection)-[:HAS]->(sParent:Statement)
       

        // statement

        OPTIONAL MATCH (sParent)<-[:SUPPORTS|OPPOSES]-(cArg:Connection)
        
        WITH sParent, u, collect(cArg.id) as cArgs, ARG_connections, ARG_stm
        
        OPTIONAL MATCH (sParent)-[:HAS]->(cParent:Connection)
        
        WITH sParent, u, cArgs, collect(cParent.id) as cParents, ARG_connections, ARG_stm
        
        OPTIONAL MATCH (sParent)-[:TAGGED]->(t:Tag)
        WITH sParent, u, cArgs, cParents, collect(t.value) as tags, ARG_connections, ARG_stm

        OPTIONAL MATCH (u)-[uc:CREATED]->(sParent)
        OPTIONAL MATCH (u)-[r:VOTED]->(sParent)
        
        WITH sParent, u, uc, r, cArgs, cParents, tags,apoc.coll.union(
            collect({ 
                    id:sParent.id, 
                    value:sParent.value,
                    truth:sParent.truth,
                    arg_connection_ids:cArgs,
                    parent_connection_ids:cParents,
                    tags:tags,
                    user_created:uc IS NOT NULL,
                    user_voted:r.value
                }), ARG_stm) as statements, ARG_connections,ARG_stm


        // arg_connections

        WITH sParent, u, statements, ARG_connections
        OPTIONAL MATCH (sParent)<-[argSup:SUPPORTS|OPPOSES]-(cArg:Connection)<-[:HAS]-(sArg:Statement)
        OPTIONAL MATCH (u)-[uc2:CREATED]->(cArg)
        OPTIONAL MATCH (u)-[r2:VOTED]->(cArg)
        
        WITH sParent, u, statements, apoc.coll.union(collect({
            id:cArg.id, 
            stm_parent_id:sParent.id,
            stm_child_id:sArg.id,
            supports:TYPE(argSup) = "SUPPORTS",
            user_created:uc2 IS NOT NULL,
            user_voted:r2.value
        }),ARG_connections) as arg_connections, ARG_connections

        
        
        // parent_connections

        WITH sParent, u, statements, arg_connections
        OPTIONAL MATCH (sParent)-[:HAS]->(cParent:Connection)-[parentSup:SUPPORTS|OPPOSES]->(sParent2:Statement)
        OPTIONAL MATCH (u)-[uc3:CREATED]->(cParent)
        OPTIONAL MATCH (u)-[r3:VOTED]->(cParent)
        
        WITH sParent, u, statements,arg_connections, apoc.coll.union(arg_connections, collect({
            id:cParent.id, 
            stm_parent_id:sParent2.id,
            stm_child_id:sParent.id,
            supports:TYPE(parentSup) = "SUPPORTS",
            user_created:uc3 IS NOT NULL,
            user_voted:r3.value
        })) as connections

        

        RETURN collect(statements) as statements, collect(connections) as connections

      """, id=statement_id)
    success = await r.value()
    success = True
    log = "NOT YET IMPLEMENTED" if success else "Error: statement may not exist"
    print(log)
    return Response(message=log)
