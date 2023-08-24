from multiprocessing.pool import AsyncResult

from neo4j import ResultSummary

from models import User


async def user_create_tx(tx, *, username, hashed_password):
    r = await tx.run(""" 
        MERGE (c:User{username:$username})
        ON CREATE 
            SET c.hashed_password = $hashed_password
        RETURN 1
    """, username=username, hashed_password=hashed_password)

    success = await r.value()
    return "user created successfully" if success else "Error: Tag may not exist, you are not creator of statement"


async def user_delete_tx(tx, username):
    r = await tx.run("""
        MATCH (c:User{username:$username})
        DETACH DELETE c
        RETURN 1""", username=username)

    success = await r.value()
    return "user deleted successfully" if success else "Error:  you are not the User"


async def user_get_hashed_password_tx(tx, username):
    result: AsyncResult = await tx.run("""
        MATCH (c:User{username:$username})
        RETURN c.hashed_password as pw
    """, username=username)
    record = await result.single()
    return record["pw"]


async def user_modify_star_tx(tx, *, username, object_id, _type="Tag|Statement|User", removestar=False):
    _type = _type.capitalize()
    if _type not in ["Tag", "Statement", "User", "Tag|Statement|User"]:
        raise Exception("Invalid Object of Label value " + _type)
    q = f"""
            MATCH (u:User{{username:$username}})
            MATCH (o:{_type}{{id:$id}})
            """ + "MERGE (u)-[r:STARED]->(o)" if not removestar else """
            MATCH (u)-[r:STARED]->(o)
            DELETE r
            RETURN 1"""

    r = await tx.run(q, username=username, removestar=removestar, id=object_id, )
    success = await r.value()
    return "star modified successfully" if success else "Error: Tag|Statement|User may not exist"


async def user_report_tx(tx, *, object_id, reason="", _type="Tag|Statement|User", ):
    _type = _type.capitalize()
    if _type not in ["Tag", "Statement", "User", "Tag|Statement|User"]:
        raise Exception("Invalid Label value " + _type)
    r = await tx.run(f"""
            MATCH (o:{_type}{{id:$object_id}})
            OPTIONAL MATCH (o)<-[r:REPORTED]-(:Report)
            WITH r WHERE r is Null
            MERGE (o)<-[r:REPORTED{{message:$message}}]-(:Report)
            RETURN 1
            """, object_id=object_id, message=reason)
    success = await r.value()
    return "X reported successfully" if success else "Error: X may not exist"


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


async def user_changepassword_tx(tx, *, username, password):
    result = await tx.run("""
            MATCH (c:User{username:$username})
            SET c.hashed_password = $hashed_pw
            RETURN 1
        """, username=username, hashed_pw=password)

    success = await result.value()
    return "password changed successfully " if success else "Error: You are not the User"
