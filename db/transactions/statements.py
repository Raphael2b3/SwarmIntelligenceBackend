from uuid import uuid4

# ? Maby get user from db call bookmark before, because there will always be a validation for the  user before this call
from neo4j import ResultSummary

from db.dbcontroller import IndexesAndConstraints


async def statement_create_tx(tx, *, text, username, ):
    r = await tx.run("""
        MATCH (u:User{username:$username})
        OPTIONAL MATCH (p:Statement{value:$text})
        WITH p, u WHERE p IS NULL
        MERGE (u)-[:CREATED]->(:Statement{value:$text,id:$id})
        RETURN 1
        """, text=text, username=username, id=str(uuid4()))
    success = await r.value()
    return "statement created successfully" if success[
        0] else "Error: statement already exist"


async def statement_delete_tx(tx, *, statement_id, username):
    r = await tx.run("""
            MATCH (p:Statement{id:$id})<-[:CREATED]-(:User{username:$username})
            WITH p
            DETACH DELETE p
            RETURN
            """, id=statement_id, username=username)
    success = await r.value()
    return "statement deleted successfully" if success[
        0] else "Error: statement may not exist, you are not creator of statement"


async def statement_get_many_tx(tx, *, query_string, n_results=10, skip=0):
    result = await tx.run("""
            CALL db.index.fulltext.queryNodes($index, $query_string,{
                skip:$skip,
                limit:$limit
            }) YIELD node, score
            return node.value as value, node.id as id
            """, query_string=query_string, limit=n_results, skip=skip, index=IndexesAndConstraints.statementsAndTags)
    return [dict(record) for record in await result.fetch(n_results)]


async def statement_modify_tag_tx(tx, *, username, statement_id, tags):  # TODO Iterate thru tags with Cypher to
    # TODO  modify multiply tags, not working sofar
    r = await tx.run("""
    PROFILE
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$id})
            MATCH (p:Tag{value:$tag})
            WITH *
            WHERE (u)-[:CREATED]->(s)
            MATCH (s)-[r:Tag]->(p)
            DELETE r
            
    """, username=username, id=statement_id, tag=tags)
    summary: ResultSummary = await r.consume()
    return summary.profile


async def statement_vote_tx(tx, *, username, statement_id, vote):
    r = await tx.run("""
    PROFILE
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$id})
            MERGE (u)-[v:VOTED]->(s)
            SET v.value= $vote
    """, username=username, id=statement_id, vote=vote)
    summary: ResultSummary = await r.consume()
    return summary.profile


# TODO calculate Truth-Value with txs
async def calc_w():
    q = """
    PROFILE
    MATCH (p:Statement)
    WHERE NOT (p)<--(:Connection)
    WITH p
    MATCH (p)-[:HAS]->(:Connection)-->(i:Statement)
    WITH *
    """
    r = None
    return

    summary: ResultSummary = await r.consume()
    return summary.profile

# TODO user notifactions to improve all queries

# TODO make it work: get_context
async def statement_get_context_tx(tx, *, statement_id, exclude_ids):  # generiere context

    r = await tx.run("""PROFILE 
        MATCH (s:Statement{id:$statement_id})
        UNWIND [1,2,3,4,5] as x
        return x as A
        UNION
        MATCH (s)-[:HAS]->(c:Connection)-->(d:Statement)
        RETURN d as A
        
    """, statement_id=statement_id)
    print("HAHAHSXXSAD:::    ", *[dict(s for s in await r.fetch(100))])
    summary: ResultSummary = await r.consume()
    return summary.profile
    return None


""" 
async def statement_get_full_context_tx(tx, *, statement_id, username, parent_gens=1, n_parents=3, skip_parents=0,
                                        child_gens=1,
                                        n_children=8, skip_children=0, ):  # generiere context

    result = await tx.run(""" """, )

    return StatementContext()
"""
