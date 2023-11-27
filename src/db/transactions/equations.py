from db.core import transaction
from models.responses import Response


@transaction
async def equation_get_many(tx, *, query, limit=10, skip=0):
    result = await tx.run("""
                    
                    CALL {
                        MATCH (a:Equation)
                        WHERE a.id = $id
                        RETURN a
                    UNION
                        MATCH (a:Equation)-[:EQUALS]->(s:Statement)
                        WHERE s.id = $id
                        RETURN a
                    }
                    
                    MATCH (a)-[:EQUALS]->(s:Statement)
                    RETURN {id:a.id, value:collect({ id: s.id, message: s.value })} as equations
                    SKIP $skip
                    LIMIT $limit
                        
                """, id=query, limit=limit, skip=skip)

    return Response(message="200", value=[dict(record) for record in await result.fetch(limit)])
