from uuid import uuid4

import db.settings
from db.core import transaction
from neo4j import AsyncResult, Record


@transaction
async def statement_create(tx, *, text, username, tags=()):
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
    return {"message": log, "value": {**dict(success), "value": text}}


@transaction
async def statement_delete(tx, *, statement_id, username):
    r = await tx.run("""
            MATCH (p:Statement{id:$id})<-[:CREATED]-(:User{username:$username})
            WITH p
            DETACH DELETE p
            RETURN 1 
            """, id=statement_id, username=username)
    success = await r.value()
    log = "statement deleted successfully" if success else "Error: statement may not exist, you are not creator of statement"
    print(log)
    return {"message": log}


@transaction
async def statement_get_many(tx, *, query_string, n_results=10, skip=0, tags=()):
    await tx.run("""CALL db.index.fulltext.awaitEventuallyConsistentIndexRefresh()
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
            
            """, query_string=query_string, limit=n_results, skip=skip, index=db.settings.Index.statementsFullText)
    log = "success"
    return {"message": log, "value": [dict(record) for record in await result.fetch(n_results)]}


@transaction
async def statement_modify_tag(tx, *, username, statement_id, tags):
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
    return {"message": log}


@transaction
async def statement_vote(tx, *, username, statement_id, vote):
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
    return {"message": log}


@transaction
async def statement_get_context(tx, *, statement_id, exclude_ids, username):
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
            OPTIONAL MATCH (u)-[r2:WEIGHTED]->(cArg) // check for user voted connection
        
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
            OPTIONAL MATCH (u)-[r3:WEIGHTED]->(cParent)
        
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
                OPTIONAL MATCH (u)-[r2:WEIGHTED]->(cArg) // check for user voted connection
        
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
                OPTIONAL MATCH (u)-[r3:WEIGHTED]->(cParent)
        
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
                OPTIONAL MATCH (u)-[r2:WEIGHTED]->(cArg) // check for user voted connection
        
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
                OPTIONAL MATCH (u)-[r3:WEIGHTED]->(cParent)
        
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
    return {"message": log, "value": {"connections": rec["connections"], "statements": rec["statements"]}}

@transaction
async def statement_calculate_truth(tx):
    """
        1 generate root nodes truth and generate and return connections of schema {weight, parent_id, weighted_truth}
        2 generate dict of scheme parent_id:number_of_known_weights -> return nodes which id and input grade is equal to
            parent_id and number_of_known_weights:
        3. generate truth for node, delete connections used for the truth generation

        4. save truth to db and return connections of schema {weight, parent_id, weighted_truth}

        5. if there are connections returned start from 2.

    """

    r: AsyncResult = await tx.run("""
// generate root nodes truth and generate and return connections of schema {weight, parent_id, weighted_truth}

MATCH (a:Statement) 
WHERE NOT (a)<-[:SUPPORTS|OPPOSES]-(:Connection) // Definition of Root notes

// generate truth and set it
MATCH (a)<-[v:VOTED]-(:User)

WITH avg(v.value) as truth, a
SET a.truth = truth

// generate connections
WITH a, truth
MATCH (a)-[:HAS]->(c:Connection)-[r:OPPOSES|SUPPORTS]->(b:Statement)
WITH truth, c, b.id as parent_id, CASE 
    WHEN TYPE(r) = "OPOSSES" THEN -1 
    ELSE 1 END 
    as sign
    
MATCH (c)<-[v:VOTED]-(:User)

WITH avg(v.value) as uweight, truth, parent_id, sign

WITH uweight*sign as weight, uweight * truth * sign as weighted_truth, parent_id

RETURN collect({parent_id:parent_id,weight:weight, weighted_truth:weighted_truth}) as connections
""")

    data = (await r.single())["connections"]
    connections = {}
    iterations = 1
    while len(data):
        print(data)
        for con in data:
            if not con["parent_id"] in connections:
                connections[con["parent_id"]] = []
            connections[con["parent_id"]].append({i: con[i] for i in con if i != "parent_id"})

        grades = {con: len(connections[con]) for con in connections}
        ids = [key for key in connections]
        print("Grades", grades)
        print("Data", connections)

        # Method 1 match statements where the id is in the list,

        r: AsyncResult = await tx.run("""
        // return node ids which id and input grade is equal to parent_id and number_of_known_weights
            
        WITH $ids as ids, $grades as grades // ids is list of ids, grades is dictionary parent_id:known_grade
        
        // match statements
        MATCH (a:Statement)
        WHERE a.id IN ids
        
        // get grade and filter ids
        MATCH (a)<-[r:SUPPORTS|OPPOSES]-(:Connection)
        WITH a, count(r) as grade, grades
        WITH a
        WHERE grades[a.id] = grade
        
        // generate voted truth
        MATCH (a)<-[v:VOTED]-(:User)
        WITH avg(v.value) as truth, a
        
        RETURN collect([a.id, truth]) as truths
        """, ids=ids, grades=grades)
        data = await r.single()
        truths = data["truths"]
        weighted_truth = {}
        for truth in truths:
            id = truth[0]
            weighted_truth[id] = truth_of_node(connections.pop(id), truth[1])

        r: AsyncResult = await tx.run("""
                
                // generate truth for node, delete connections used for the truth generation

                WITH $truths as truth

                UNWIND keys(truth) as id
                MATCH (a:Statement)
                WHERE a.id = id
                SET a.truth = truth[id]

                // generate connections
                WITH a, truth[id] as truth
                MATCH (a)-[:HAS]->(c:Connection)-[r:OPPOSES|SUPPORTS]->(b:Statement)
                WITH truth, c, r, b.id as parent_id, CASE 
                    WHEN TYPE(r) = "OPOSSES" THEN -1 
                    ELSE 1 END 
                    as sign
                WITH c, sign, truth, parent_id
                MATCH (c)<-[v:VOTED]-(:User)

                WITH avg(v.value) as uweight, truth, parent_id, sign

                WITH uweight*sign as weight, uweight * truth * sign as weighted_truth, parent_id

                RETURN collect({parent_id:parent_id,weight:weight, weighted_truth:weighted_truth}) as connections


                """, truths=weighted_truth)
        data = (await r.single())["connections"]
        iterations += 1
    return {"message": f"Success. Needed {iterations} Iterations"}
