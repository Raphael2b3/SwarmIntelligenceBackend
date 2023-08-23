from contextlib import asynccontextmanager

from neo4j import AsyncGraphDatabase, AsyncDriver

from env import DB_CONNECTION_STRING, DB_PASSWORD, DB_USERNAME


# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

class IndexesAndConstraints:
    statementsAndTags = "StatementsAndTags"
    statementId = "StatementId"
    tagId = "TagId"
    connectionId = "ConnectionId"
    username = "Username"


class Database:
    driver: AsyncDriver
    URI = DB_CONNECTION_STRING
    AUTH = (DB_USERNAME, DB_PASSWORD)
    DATABASE = "neo4j"
    createIndexes = False

    @classmethod
    async def create_indexes(cls, session):
        await session.run("""
                                CREATE FULLTEXT INDEX StatementsAndTags IF NOT EXISTS
                                FOR (n:Statement|Tag)
                                ON EACH [n.value]
                                OPTIONS {
                                      indexConfig: {
                                        `fulltext.analyzer`: 'german',
                                        `fulltext.eventually_consistent`: true
                                      }
                                }
                                """)

        await session.run("""
                                CREATE RANGE INDEX StatementId IF NOT EXISTS
                                FOR (n:Statement)
                                ON (n.id) """)

        await session.run("""
                                CREATE RANGE INDEX TagId IF NOT EXISTS
                                FOR (n:Tag)
                                ON (n.id)""")

        await session.run("""
                                CREATE RANGE INDEX ConnectionId IF NOT EXISTS
                                FOR (n:Connection)
                                ON (n.id)""")

        await session.run("""
                                CREATE TEXT INDEX Username IF NOT EXISTS
                                FOR (n:User)
                                ON (n.username)""")

    @classmethod
    async def create_constraints(cls, session):
        await session.run("""
                                CREATE FULLTEXT INDEX StatementsAndTags IF NOT EXISTS
                                FOR (n:Statement|Tag)
                                ON EACH [n.value]
                                OPTIONS {
                                      indexConfig: {
                                        `fulltext.analyzer`: 'german',
                                        `fulltext.eventually_consistent`: true
                                      }
                                }
                                """)

        await session.run("""
                                CREATE RANGE INDEX StatementId IF NOT EXISTS
                                FOR (n:Statement)
                                ON (n.id) """)

        await session.run("""
                                CREATE RANGE INDEX TagId IF NOT EXISTS
                                FOR (n:Tag)
                                ON (n.id)""")

        await session.run("""
                                CREATE RANGE INDEX ConnectionId IF NOT EXISTS
                                FOR (n:Connection)
                                ON (n.id)""")

        await session.run("""
                                CREATE TEXT INDEX Username IF NOT EXISTS
                                FOR (n:User)
                                ON (n.username)""")

    @classmethod
    async def init(cls):
        cls.driver = AsyncGraphDatabase.driver(uri=cls.URI, auth=cls.AUTH, database=cls.DATABASE)
        if not cls.createIndexes: return
        async with cls.session() as session:
            await cls.create_indexes(session)

    @classmethod
    async def close(cls):
        await cls.driver.close()

    @classmethod
    @asynccontextmanager
    async def session(cls):
        session = cls.driver.session(database=cls.DATABASE)
        try:
            yield session
        finally:
            await session.close()


async def db_session():
    with Database.session() as s:
        yield s
