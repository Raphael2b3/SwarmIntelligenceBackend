from uuid import uuid4


# ? Maby get user from db call bookmark before, because there will always be a validation for the  user before this call
async def statement_create_tx(tx, *, text, username, ):
    await tx.run("""
        MATCH (u:User{username:$username})
        OPTIONAL MATCH (p:Statement{value:$text})
        WITH p, u WHERE p IS NULL
        MERGE (u)-[:CREATED]->(:Statement{value:$text,id:$id})
        """, text=text, username=username, id=str(uuid4()))


async def statement_delete_tx(tx, *, statement_id, username):
    await tx.run("""
            MATCH (p:Statement{id:$id})<-[:CREATED]-(:User{username:$username})
            DETACHE DELETE p
            """, id=statement_id, username=username)


async def statement_get_many_tx(tx, *, query_string, n_results=10, skip=0):  # TODO String search in db, string indexing
    # TODO Find out how SKIP works
    result = await tx.run("""
            MATCH (p:Statement)
            WHERE p.value STARTS WITH $query_string
            return p.value as value, p.id as id
            """, query_string=query_string)
    return [dict(record) async for record in await result.fetch(n_results)]


async def statement_modify_tag_tx(tx, *, username, statement_id, tags):  # TODO Iterate thru tags with Cypher to
    #  modify multiply tags
    raise Exception("Not yet implemented")
    await tx.run("""
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$id})
            MATCH (p:Tag{value:$tag})
            WITH *
            WHERE (u)-[:CREATED]->(s)
            
    """, username=username, id=statement_id, tag=tags)


async def statement_vote_tx(tx, *, username, statement_id, vote):
    await tx.run("""
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$id})
            MERGE (u)-[v:VOTED]->(s)
            SET v.value= $vote
    """, username=username, id=statement_id, vote=vote)


# TODO calculate Truth-Value with txs
def calc_w():
    q = """
    MATCH (p:Statement)
    WHERE NOT (p)<--(:Connection)
    WITH p
    MATCH (p)-[:HAS]->(:Connection)-->(i:Statement)
    WITH *
    """


# TODO make it work: get_context
async def statement_get_context_tx(tx, *, statement_id, exclude_ids):  # generiere context

    result = await tx.run(""" """, )

    return StatementContext()


# TODO Evaluate if this is needed
""" 
async def statement_get_full_context_tx(tx, *, statement_id, username, parent_gens=1, n_parents=3, skip_parents=0,
                                        child_gens=1,
                                        n_children=8, skip_children=0, ):  # generiere context

    result = await tx.run(""" """, )

    return StatementContext()
"""
