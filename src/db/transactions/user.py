from db.core import transaction


@transaction
async def user_create(tx, *, username, hashed_password):
    r = await tx.run(""" 
            MATCH (c:User{username:$username})
            RETURN 1
        """, username=username)
    success = await r.value()
    log = "Error: Username is already used by someone else"
    if not success:
        r = await tx.run(""" 
            MERGE (c:User{username:$username})
            ON CREATE 
                SET c.hashed_password = $hashed_password
            RETURN 1
        """, username=username, hashed_password=hashed_password)
        success = await r.value()

        log = "user created successfully" if success else "Error: Fatal Internal Error"
    print(log)
    return {"message": log}


@transaction
async def user_delete(tx, username):
    r = await tx.run("""
        MATCH (c:User{username:$username})
        DETACH DELETE c
        RETURN 1""", username=username)

    success = await r.value()
    log = "user deleted successfully" if success else "Error: you are not the User"
    print(log)
    return {"message": log}


@transaction
async def user_get_hashed_password(tx, username):
    result = await tx.run("""
        MATCH (c:User{username:$username})
        RETURN c.hashed_password as pw
    """, username=username)
    record = await result.single()
    return record["pw"]


@transaction
async def user_modify_star(tx, *, username, object_id, _type="Tag|Statement|User", removestar=False):
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
    log = "star modified successfully" if success else "Error: Tag|Statement|User may not exist"
    print(log)
    return {"message": log}


@transaction
async def user_report(tx, *, object_id, reason="", _type="Tag|Statement|User", ):
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
    log = "reported successfully" if success else "Error: id may not exist"
    print(log)
    return {"message": log}


@transaction
async def user_get(tx, *, username):
    result = await tx.run("""
            MATCH (c:User{username:$username})
            RETURN c.disabled as disabled, c.username as username
        """, username=username)
    try:
        r = await result.single()
        return r
    except Exception as e:
        print(e)
        return None


@transaction
async def user_change_password(tx, *, username, password):
    result = await tx.run("""
            MATCH (c:User{username:$username})
            SET c.hashed_password = $hashed_pw
            RETURN 1
        """, username=username, hashed_pw=password)

    success = await result.value()
    log = "password changed successfully " if success else "Error: You are not the User"
    print(log)
    return {"message": log}
