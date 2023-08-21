from multiprocessing.pool import AsyncResult

from neo4j import Record

from models.user import User, Vote


# TODO Make username in db unique
async def user_create_tx(tx, *, username, hashed_password):
    await tx.run(""" 
    MERGE (c:User{username:$username})
    WITH c 
    SET c.hashed_password = $hashed_password
    """, username=username, hashed_password=hashed_password)


# TODO IF bookmarks work, use it here as well
async def user_delete_tx(tx, username):
    await tx.run("""
        MATCH (c:User{username:$username})
        DELETE c""", username=username)


async def user_get_hashed_password_tx(tx, username):
    result: AsyncResult = await tx.run("""
        MATCH (c:User{username:$username})
        RETURN c.hashed_password
    """, username=username)
    record = await result.value()
    return record[0]


async def user_modify_star_tx(tx, *, username, object_id, _type="Tag|Statement|User", removestar=False):
    _type = _type.capitalize()
    if _type not in ["Tag", "Statement", "User", "Tag|Statement|User"]:
        raise Exception("Invalid Object of Label value " + _type)
    q = f"""
            MATCH (u:User{{username:$username}})
            MATCH (o:{_type}{{id:$id}})
            """ + "MERGE (u)-[r:STARED]->(o)" if not removestar else """
            MATCH (u)-[r:STARED]->(o)
            DELETE r"""

    await tx.run(q, username=username, removestar=removestar, id=object_id, )


async def user_report_tx(tx, *, object_id, reason="", _type="Tag|Statement|User", ):
    _type = _type.capitalize()
    if _type not in ["Tag", "Statement", "User", "Tag|Statement|User"]:
        raise Exception("Invalid Label value " + _type)
    await tx.run(f"""
            MATCH (o:{_type}{{id:$object_id}})
            OPTIONAL MATCH (o)<-[r:REPORTED]-(:Report)
            WITH r WHERE r is Null
            MERGE (o)<-[r:REPORTED{{message:$message}}]-(:Report)
            """, object_id=object_id, message=reason)


async def user_get_tx(tx, *, username):
    result = await tx.run("""
            MATCH (c:User{username:$username})
            RETURN c.disabled as disabled, c.username as username
        """, username=username)
    try:
        r = await result.single()
        return User(**r)
    except Exception as e:
        print(e)
        return None

