import math

from uuid import uuid4

# ? Maby get user from db call bookmark before, because there will always be a validation for the  user before this call
from neo4j import ResultSummary, AsyncResult, Record

from db.dbcontroller import IndexesAndConstraints
from models.responses import Response, Statement, Context

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


async def statement_get_many_tx(tx, *, query_string, n_results=10, skip=0, tags=()):
    print("statement get", query_string, n_results, skip, tags)  # TODO filter by tags
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


async def statement_get_context_tx(tx, *, statement_id, exclude_ids, username):
    r = await tx.run("""
        MATCH (a:Statement) WHERE a.id = $id     // find root statement
        OPTIONAL MATCH (u:User) WHERE u.username=$username // find optional user
        
        /// ROOT 
        CALL {
            WITH a, u
            WITH a, u WHERE NOT a.id IN $exclude_ids
            // statement
            OPTIONAL MATCH (a)<-[:SUPPORTS|OPPOSES]-(cArg:Connection)                   // find optional argument connections
            
            WITH a, u, collect(cArg.id) as cArgs                                        // put the found connection ids into a list
            
            OPTIONAL MATCH (a)-[:HAS]->(cParent:Connection)                             // find optional parent connections
            
            WITH a, u, cArgs, collect(cParent.id) as cParents                           // put the found connection ids into a list
            
            OPTIONAL MATCH (a)-[:TAGGED]->(t:Tag)                                       // find tags for statement
            
            WITH a, u, cArgs, cParents, collect(t.value) as tags                        // put the tags into a list
            OPTIONAL MATCH (u)-[uc:CREATED]->(a)                                        // check for statement CREATED by user
            OPTIONAL MATCH (u)-[r:VOTED]->(a)                                           // check for statement VOTED by user
            
            RETURN collect({
                id:a.id, 
                value:a.value,
                truth:a.truth,
                arg_connection_ids:cArgs,
                parent_connection_ids:cParents,
                tags:tags,
                user_created:uc IS NOT NULL,
                user_voted:r.value
            }) as root_stm
        }
        
        // arg_connection
        CALL {
            WITH a, u
            MATCH (a)<-[argSup:SUPPORTS|OPPOSES]-(cArg:Connection)<-[:HAS]-(sArg:Statement) // get argument statements
            WHERE NOT cArg.id IN $exclude_ids
            OPTIONAL MATCH (u)-[uc2:CREATED]->(cArg) // check for user created connection
            OPTIONAL MATCH (u)-[r2:VOTED]->(cArg) // check for user voted connection
        
            RETURN {
            id:cArg.id, 
                stm_parent_id:a.id,
                stm_child_id:sArg.id,
                supports:TYPE(argSup) = "SUPPORTS",
                user_created:uc2 IS NOT NULL,
                user_voted:r2.value
            } as connections
        
        UNION // parent_connection
                
            WITH a, u
            MATCH (a)-[:HAS]->(cParent:Connection)-[parentSup:SUPPORTS|OPPOSES]->(sParent:Statement)
            WHERE NOT cParent.id IN $exclude_ids
            
            OPTIONAL MATCH (u)-[uc3:CREATED]->(cParent)
            OPTIONAL MATCH (u)-[r3:VOTED]->(cParent)
        
            RETURN {
                id:cParent.id, 
                stm_parent_id:sParent.id,
                stm_child_id:a.id,
                supports:TYPE(parentSup) = "SUPPORTS",
                user_created:uc3 IS NOT NULL,
                user_voted:r3.value
            } as connections
        }
        
        WITH a, u, root_stm, collect(connections) as root_connections
        
        CALL{
            
            // ARG Statements
            
            WITH a, u
            MATCH (a)<-[:SUPPORTS|OPPOSES]-(:Connection)<-[:HAS]-(sArg:Statement)
            
            WITH u, sArg as a
            
            CALL {
                WITH a, u
                WITH a, u WHERE NOT a.id IN $exclude_ids
                // Statement to dict
                OPTIONAL MATCH (a)<-[:SUPPORTS|OPPOSES]-(cArg:Connection)                   // find optional argument connections
            
                WITH a, u, collect(cArg.id) as cArgs                                        // put the found connection ids into a list
            
                OPTIONAL MATCH (a)-[:HAS]->(cParent:Connection)                             // find optional parent connections
            
                WITH a, u, cArgs, collect(cParent.id) as cParents                           // put the found connection ids into a list
            
                OPTIONAL MATCH (a)-[:TAGGED]->(t:Tag)                                       // find tags for statement
            
                WITH a, u, cArgs, cParents, collect(t.value) as tags                        // put the tags into a list
                OPTIONAL MATCH (u)-[uc:CREATED]->(a)                                        // check for statement CREATED by user
                OPTIONAL MATCH (u)-[r:VOTED]->(a)                                           // check for statement VOTED by user
            
                RETURN {                          // todo minimate
                    id:a.id, 
                    value:a.value,
                    truth:a.truth,
                    arg_connection_ids:cArgs,
                    parent_connection_ids:cParents,
                    tags:tags,
                    user_created:uc IS NOT NULL,
                    user_voted:r.value
                } as root_stm
            }
        
        
            // arg_connection
            CALL {
                WITH a, u
                MATCH (a)<-[argSup:SUPPORTS|OPPOSES]-(cArg:Connection)<-[:HAS]-(sArg:Statement) // get argument statements
                WHERE NOT cArg.id IN $exclude_ids
            
                OPTIONAL MATCH (u)-[uc2:CREATED]->(cArg) // check for user created connection
                OPTIONAL MATCH (u)-[r2:VOTED]->(cArg) // check for user voted connection
        
                RETURN {
                id:cArg.id, 
                    stm_parent_id:a.id,
                    stm_child_id:sArg.id,
                    supports:TYPE(argSup) = "SUPPORTS",
                    user_created:uc2 IS NOT NULL,
                    user_voted:r2.value
                } as connections
        
            UNION // parent_connection
                    
                WITH a, u
                MATCH (a)-[:HAS]->(cParent:Connection)-[parentSup:SUPPORTS|OPPOSES]->(sParent:Statement)
                WHERE NOT cParent.id IN $exclude_ids
            
                OPTIONAL MATCH (u)-[uc3:CREATED]->(cParent)
                OPTIONAL MATCH (u)-[r3:VOTED]->(cParent)
        
                RETURN {
                    id:cParent.id, 
                    stm_parent_id:sParent.id,
                    stm_child_id:a.id,
                    supports:TYPE(parentSup) = "SUPPORTS",
                    user_created:uc3 IS NOT NULL,
                    user_voted:r3.value
                } as connections
            }
        
            RETURN root_stm as arg_statement, collect(connections) as arg_connections
        
        }
        UNWIND arg_connections as arg_con
        
        WITH a, u, root_stm, arg_statement,root_connections, collect(arg_con) as arg_connections
        WITH a, u, root_stm, collect(arg_statement) as arg_statements, apoc.coll.union(root_connections, arg_connections) as connections
        WITH a, u, root_stm+arg_statements as statements, connections
        
        CALL {
        
            // PARENT Statements
        
            WITH a, u
            MATCH (a)-[:HAS]->(:Connection)-[:SUPPORTS|OPPOSES]->(sParent:Statement)
            WITH u, sParent as a 
            CALL {
                WITH a, u
                WITH a, u WHERE NOT a.id IN $exclude_ids
                
                // Statement to dict
                OPTIONAL MATCH (a)<-[:SUPPORTS|OPPOSES]-(cArg:Connection)                   // find optional argument connections
            
                WITH a, u, collect(cArg.id) as cArgs                                        // put the found connection ids into a list
            
                OPTIONAL MATCH (a)-[:HAS]->(cParent:Connection)                             // find optional parent connections
            
                WITH a, u, cArgs, collect(cParent.id) as cParents                           // put the found connection ids into a list
            
                OPTIONAL MATCH (a)-[:TAGGED]->(t:Tag)                                       // find tags for statement
            
                WITH a, u, cArgs, cParents, collect(t.value) as tags                        // put the tags into a list
                OPTIONAL MATCH (u)-[uc:CREATED]->(a)                                        // check for statement CREATED by user
                OPTIONAL MATCH (u)-[r:VOTED]->(a)                                           // check for statement VOTED by user
            
                RETURN {                         
                    id:a.id, 
                    value:a.value,
                    truth:a.truth,
                    arg_connection_ids:cArgs,
                    parent_connection_ids:cParents,
                    tags:tags,
                    user_created:uc IS NOT NULL,
                    user_voted:r.value
                } as root_stm
            }
        
        
            // arg_connection
            CALL {
                WITH a, u
                MATCH (a)<-[argSup:SUPPORTS|OPPOSES]-(cArg:Connection)<-[:HAS]-(sArg:Statement) // get argument statements
                WHERE NOT cArg.id IN $exclude_ids
            
                OPTIONAL MATCH (u)-[uc2:CREATED]->(cArg) // check for user created connection
                OPTIONAL MATCH (u)-[r2:VOTED]->(cArg) // check for user voted connection
        
                RETURN {
                id:cArg.id, 
                    stm_parent_id:a.id,
                    stm_child_id:sArg.id,
                    supports:TYPE(argSup) = "SUPPORTS",
                    user_created:uc2 IS NOT NULL,
                    user_voted:r2.value
                } as connections
        
            UNION // parent_connection
                    
                WITH a, u
                MATCH (a)-[:HAS]->(cParent:Connection)-[parentSup:SUPPORTS|OPPOSES]->(sParent:Statement)
                WHERE NOT cParent.id IN $exclude_ids
            
                OPTIONAL MATCH (u)-[uc3:CREATED]->(cParent)
                OPTIONAL MATCH (u)-[r3:VOTED]->(cParent)
        
                RETURN {
                    id:cParent.id, 
                    stm_parent_id:sParent.id,
                    stm_child_id:a.id,
                    supports:TYPE(parentSup) = "SUPPORTS",
                    user_created:uc3 IS NOT NULL,
                    user_voted:r3.value
                } as connections
            }
        
            RETURN root_stm as parent_statement, collect(connections) as parent_connections
        }
        UNWIND parent_connections as parent_con
        WITH a, u, statements, parent_statement, connections, collect(parent_con) as parent_connections
        WITH a, u, statements, collect(parent_statement) as parent_statements, apoc.coll.union(connections, parent_connections) as connections
        RETURN  statements+parent_statements as statements, connections

      """, id=statement_id, username=username, exclude_ids=exclude_ids)
    try:
        rec: Record | dict = await r.single(strict=True)
        log = "Success"

    except Exception as e:
        rec = {"connections": None, "statements": None}
        print(e)
        log = "Error: Getting context failed statement may not exist"
    print(log)
    return Response(message=log, value=Context(connections=rec["connections"], statements=rec["statements"]))


async def statement_calculate_truth_tx(tx):
    # TODO calc truth :=)

    next_connections = []
    cached_truth = {}

    # get leaf statements and calculate their base truth : gen 0

    # get all statements 1 hop away from the leafs and calculate their base truth : gen 1

    # for each connection between gen 0 and gen 1 get the weight and multiply it with the truth of the gen 0