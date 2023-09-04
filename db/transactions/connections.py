from uuid import uuid4

from neo4j import ResultSummary, AsyncResult

from models.responses import DefaultResponse

from builtins import print as _print


def print(*args, **kwargs):
    _print("TX: ", *args, "\n", **kwargs)


# TODO return DefaultResponse everytime

async def connection_create_tx(tx, *, stop_id, start_id, is_support, username):
    support_str = "SUPPORTS" if is_support else "OPPOSES"
    query = f"""
    MATCH (a:Statement{{id:$start_id}}) 
    MATCH (b:Statement{{id:$stop_id}})
    WITH a, b
    WHERE NOT (b)-[*]->(a)
    OPTIONAL MATCH (a)-[:HAS]->(c:Connection)-[:SUPPORTS|OPPOSES]->(b)
    CALL{{
            WITH c
            WITH c
            WHERE c IS NOT NULL
            RETURN c.id as id,  FALSE as created 
        UNION
            WITH *
            WITH * 
            WHERE c IS NULL
            CREATE (a)-[:HAS]->(n:Connection{{id:$new_id}})-[:{support_str}]->(b)
            WITH n
            MATCH (u:User{{username:$username}})
            CREATE (u)-[:CREATED]->(n)
            RETURN $new_id as id, TRUE as created
    }}
    RETURN *
    """
    r: AsyncResult = await tx.run(query, start_id=start_id, stop_id=stop_id, new_id=str(uuid4()), username=username)
    success = await r.single()
    log = "connection created successfully" if success[
        "created"] else "Error: statement may not exist, connection already exists or argument cicle"
    print(log)
    return DefaultResponse(message=log, value=success["id"])


async def connection_delete_tx(tx, *, connection_id, username):
    r = await tx.run("""
            MATCH (c:Connection{id:$id})
            MATCH (u:User{username:$username})
            WHERE (u)-[:CREATED]->(c) 
            DETACH DELETE (c)
            RETURN 1
            """, id=connection_id, username=username)
    success = await r.value()
    log = "connection deleted successfully" if success else "Error: connection may not exist, you are not creator of connection"
    print(log)
    return log


async def connection_weight_tx(tx, *, connection_id, weight, username):
    r = await tx.run("""
        MATCH (c:Connection{id: $id})
        MATCH (u:User{username:$username})
        MERGE (u)-[r:VOTED]->(c)
        SET r.value = $weight
        RETURN 1
        """, id=connection_id, weight=weight, username=username)
    success = await r.value()
    log = "connection weighted successfully" if success else "Error: connection may not exist"
    print(log)
    return log
