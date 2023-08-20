from uuid import uuid4


async def connection_create_tx(tx, *, stop_id, start_id, is_support, username):
    support_str = "SUPPORTS" if is_support else "OPPOSES"
    query = f"""
    MATCH (a:Statement{{id:$start_id}}) 
    MATCH (b:Statement{{id:$stop_id}})
    WITH a, b
    WHERE NOT (b)-[*]->(a) AND NOT (a)-[:HAS]->(:Connection)-->(b)
    MERGE (a)-[:HAS]->(c:Connection{{id:$new_id}})-[:{support_str}]->(b)
    WITH c
    MATCH (u:User{{username:$username}})
    MERGE (u)-[:CREATED]->(c)
    """
    await tx.run(query, start_id=start_id, stop_id=stop_id, new_id=str(uuid4()), username=username)


async def connection_delete_tx(tx, *, connection_id, username):
    await tx.run("""
            MATCH (c:Connection{id:$connection_id})
            MATCH (u:User{username:$username})
            WITH *
            WHERE (u)-[:CREATED]->(c) 
            DETACHE DELETE (c)
            """, connection_id=connection_id, username=username)


async def connection_weight_tx(tx, *, connection_id, is_bad, username):
    await tx.run("""
        MATCH (c:Connection{id: $connection_id})
        MATCH (u:User{username:$username})
        MERGE (u)-[r:WEIGHT]->(c)
        SET r.is_bad = $is_bad
        """, connection_id=connection_id, is_bad=is_bad, username=username)
