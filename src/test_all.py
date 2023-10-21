import pytest
from starlette.testclient import TestClient

from db.dbcontroller import Database as Db
import routes.users as userroute
import routes.default as defaultroute
import routes.tags as tagroute
import routes.statements as statementroute
import routes.connections as connectionroute
import security.jwt_auth as auth

#watch("neo4j", out=sys.stdout)

STATEMENT = TAG = USERNAME = PASSWORD = "test"
STATEMENT_SEARCH = STATEMENT2 = TAG_SEARCH = "t"
TEST_URI = "neo4j://localhost:7687"
TEST_AUTH = "neo4j", "00000000"
TEST_DB = "neo4j"

pytest_plugins = ('pytest_asyncio',)


def converter(o):
    return o


def ident(o): return o


async def test(title, func, conv=converter):
    print(title)
    r = conv(await func())
    print(r)
    assert r
    return r

async def txs(tx):
    await tx.run("""match(a) return a""")
    r = await tx.run("""WITH a return a""")
    print(await r.values())
async def test_sesion():
    await Db.init()
    async with Db.session() as session:
        session.execute_read(txs)
    pass
@pytest.mark.asyncio
async def test_app():
    """ Db.URI = TEST_URI
    Db.AUTH = TEST_AUTH
    Db.DATABASE = TEST_DB
    Db.createIndexes = True"""
    await Db.init()
    try:
        pass
    finally:
        await Db.close()
