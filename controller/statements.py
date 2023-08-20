from models.context import StatementContext
from uuid import uuid4


# ? Maby get user from db call bookmark before, because there will always be a validation for the  user before this call
async def statement_create_tx(tx, *, text, username, ):
    await tx.run("""
        MATCH (u:User{username:$username})
        OPTIONAL MATCH (p:Statement{value:$text})
        WITH p, u WHERE p IS NULL
        MERGE (u)-[:CREATED]->(:Statement{value:$text,id:$new_id})
        """, text=text, username=username, new_id=str(uuid4()))


async def statement_delete_tx(tx, *, statement_id, username):
    await tx.run("""
            MATCH (p:Statement{id:statement_id})<-[:CREATED]-(:User{username:$username})
            DETACHE DELETE p
            """, statement_id=statement_id, username=username)


async def statement_get_many_tx(tx, *, query_string, n_results=10, skip=0):  # TODO String search in db, string indexing
    # TODO Find out how SKIP works
    result = await tx.run("""
            MATCH (p:Statement)
            WHERE p.value STARTS WITH $query_string
            return p.value as value, p.id as id
            """, query_string=query_string)
    return [dict(record) async for record in await result.fetch(n_results)]


async def statement_modify_project_tag_tx(tx, *, username, statement_id, projectname, remove):
    q = """
            MATCH (u:User{username:$username})
            MATCH (s:Statement{id:$statement_id})
            MATCH (p:Project{value:$projectname})
            WITH *
            WHERE (u)-[:CREATED]->(s)
    """ + "MATCH (s)-[r:IN]->(p) \r\n DELETE r" if remove else "MERGE (s)-[:IN]->(p)"
    await tx.run(q, username=username, statement_id=statement_id, projectname=projectname)


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
async def statement_get_context_tx(tx, *, statement_id, username, parent_gens=1, n_parents=3, skip_parents=0,
                                   child_gens=1,
                                   n_children=8, skip_children=0, ):  # generiere context

    result = await tx.run(""" """, )

    return StatementContext()
