import asyncio
import pytest
import routes.users
from db.dbcontroller import Database as Db
import routes.users as userroute
import routes.default as defaultroute
import routes.tags as tagroute
import routes.statements as statementroute
import routes.connections as connectionroute
import security.jwt_auth as auth

import sys
from neo4j.debug import watch
watch("neo4j", out=sys.stdout)

STATEMENT = TAG = USERNAME = PASSWORD = "test"
STATEMENT_SEARCH = STATEMENT2 = TAG_SEARCH = "t"
TEST_URI = "neo4j://localhost:7687"
TEST_AUTH = "neo4j", "00000000"
TEST_DB = "neo4j"

pytest_plugins = ('pytest_asyncio',)


def converter(o):
    return o["args"]["string-representation"]


def ident(o): return o


async def test(title, func, conv=converter):
    print(title)
    r = conv(await func())
    print(r)
    assert r
    return r


@pytest.mark.asyncio
async def test_app():
    Db.URI = TEST_URI
    Db.AUTH = TEST_AUTH
    Db.DATABASE = TEST_DB
    Db.createIndexes = True
    await Db.init()

    await test("db connectivity and auth...", lambda: Db.driver.verify_authentication(), ident)

    await test("creating test user",
               lambda: userroute.create(body=userroute.RequestUserCreate(username=USERNAME, password=PASSWORD)))

    token = await test("getting access Token", lambda: defaultroute.login_for_access_token(
        defaultroute.OAuth2PasswordRequestForm(password=PASSWORD, username=USERNAME)), ident)

    user = await test("getting User From DB", lambda: auth.get_current_user(token["access_token"]), ident)

    await test("creating Tag",
               lambda: tagroute.create(current_user=user, body=tagroute.RequestTagCreate(value=TAG)))

    tags = await test("finding Tag", lambda: tagroute.get(body=tagroute.RequestTagSearch(q=TAG_SEARCH)), ident)

    await test("creating Statement",
               lambda: statementroute.create(current_user=user,
                                             body=statementroute.RequestStatementCreate(value=STATEMENT,
                                                                                        tags=[TAG])))
    await test("creating Statemen 2", lambda: statementroute.create(current_user=user,
                                                                    body=statementroute.RequestStatementCreate(
                                                                        value=STATEMENT2, tags=[TAG])))
    statements = await test("getting Statements", lambda: statementroute.get(current_user=user,
                                                                             body=statementroute.RequestStatementSearch(
                                                                                 q=STATEMENT_SEARCH, tags=[TAG])),
                            ident)

    await test("modifying Statement Tag", lambda: statementroute.modify_tag(current_user=user,
                                                                            body=statementroute.RequestTagSet(
                                                                                id=statements[1]["id"],
                                                                                tags=[])))

    await test("voting Statement", lambda: statementroute.vote(current_user=user,
                                                               body=statementroute.RequestStatementVote(
                                                                   id=statements[0]["id"],
                                                                   value=1)))

    await test("create Connection", lambda: connectionroute.create(current_user=user,
                                                                   body=connectionroute.RequestConnectionCreate(
                                                                       parent_id=statements[0]["id"],
                                                                       child_id=statements[1]["id"],
                                                                       supports=True)))

    # TODO Should fail
    await test("create Connection", lambda: connectionroute.create(current_user=user,
                                                                   body=connectionroute.RequestConnectionCreate(
                                                                       parent_id=statements[1]["id"],
                                                                       child_id=statements[0]["id"],
                                                                       supports=False)))
    # statement get context
    await test("getting Context", lambda: statementroute.get_context(current_user=user,
                                                                     body=statementroute.RequestContext(
                                                                         id=statements[1]["id"])))

    await test("Vote Connection", lambda: connectionroute.weight(current_user=user,
                                                                 body=connectionroute.RequestConnectionVote(
                                                                     parent_id=statements[1]["id"],
                                                                     child_id=statements[0]["id"],
                                                                     supports=False)))
    return
    # star
    # report
    await test("delete Connection", lambda: connectionroute.delete(current_user=user,
                                                                   body=connectionroute.RequestDelete(id="")))
    print("deleting Statements")
    for stm in statements:
        await test(stm["value"], lambda: statementroute.delete(current_user=user,
                                                               body=statementroute.RequestDelete(id=stm["id"])))

    await test("deleting Tag",
               lambda: tagroute.delete(current_user=user, body=tagroute.RequestDelete(id=tags[0]["id"])))

    await test("deleting test user", lambda: userroute.delete(current_user=userroute.User(username=USERNAME)))

    await Db.close()
