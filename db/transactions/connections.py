from uuid import uuid4

from neo4j import ResultSummary


async def connection_create_tx(tx, *, stop_id, start_id, is_support, username):
    support_str = "SUPPORTS" if is_support else "OPPOSES"
    query = f"""
    MATCH (a:Statement{{id:$start_id}}) 
    MATCH (b:Statement{{id:$stop_id}})
    WITH a, b
    WHERE NOT (b)-[*]->(a) AND NOT (a)-[:HAS]->(:Connection)-[:SUPPORTS|OPPOSES]->(b)
    CREATE (a)-[:HAS]->(c:Connection{{id:$new_id}})-[:{support_str}]->(b)
    WITH c
    MATCH (u:User{{username:$username}})
    CREATE (u)-[:CREATED]->(c)
    RETURN 1
    """
    r = await tx.run(query, start_id=start_id, stop_id=stop_id, new_id=str(uuid4()), username=username)
    success = await r.value()
    return "connection created successfully" if success[
        0] else "Error: statement may not exist, connection already exists or argument cicle"


async def connection_delete_tx(tx, *, connection_id, username):
    r = await tx.run("""
            MATCH (c:Connection{id:$id})
            MATCH (u:User{username:$username})
            WITH *
            WHERE (u)-[:CREATED]->(c) 
            DETACH DELETE (c)
            RETURN 1
            """, id=connection_id, username=username)
    success = await r.value()
    return "connection deleted successfully" if success[
        0] else "Error: connection may not exist, you are not creator of connection"


async def connection_weight_tx(tx, *, connection_id, is_bad, username):
    r = await tx.run("""
        MATCH (c:Connection{id: $id})
        MATCH (u:User{username:$username})
        MERGE (u)-[r:WEIGHT]->(c)
        SET r.is_bad = $is_bad
        RETURN 1
        """, id=connection_id, is_bad=is_bad, username=username)
    success = await r.value()
    return "connection weighted successfully" if success[
        0] else "Error: connection may not exist"

