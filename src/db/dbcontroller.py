from contextlib import asynccontextmanager

from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession

from env import DB_CONNECTION_STRING, DB_PASSWORD, DB_USERNAME


# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

class IndexesAndConstraints:
    tagsFullText = "TagsFulltext"
    statementsFullText = "StatementsFulltext"
    statementId = "StatementId"
    tagId = "TagId"
    connectionId = "ConnectionId"
    username = "Username"


class Database:
    driver: AsyncDriver
    URI = DB_CONNECTION_STRING
    AUTH = (DB_USERNAME, DB_PASSWORD)
    DATABASE = "neo4j"
    createIndexes = True

    # For Statements and Tags, the query ensures that a the value is Unique
    @classmethod
    async def create_indexes(cls, session):
        await session.run("""
                            CREATE FULLTEXT INDEX StatementsFulltext IF NOT EXISTS
                            FOR (n:Statement)
                            ON EACH [n.value]
                            OPTIONS {
                                  indexConfig: {
                                    `fulltext.analyzer`: 'standard',
                                    `fulltext.eventually_consistent`: true
                                  }
                            }
                            """)
        await session.run("""
                            CREATE FULLTEXT INDEX TagsFulltext IF NOT EXISTS
                            FOR (n:Tag)
                            ON EACH [n.value]
                            OPTIONS {
                                  indexConfig: {
                                    `fulltext.analyzer`: 'standard',
                                    `fulltext.eventually_consistent`: true
                                  }
                            }
                            """)

    @classmethod
    async def create_constraints(cls, session):

        await session.run("""
                CREATE CONSTRAINT StatementId IF NOT EXISTS
                FOR (a:Statement) REQUIRE a.id IS UNIQUE """)

        await session.run("""
                CREATE CONSTRAINT TagId IF NOT EXISTS
                FOR (a:Tag) REQUIRE a.id IS UNIQUE """)

        await session.run("""
                CREATE CONSTRAINT ConnectionId IF NOT EXISTS
                FOR (a:Connection) REQUIRE a.id IS UNIQUE """)

        await session.run("""
                CREATE CONSTRAINT Username IF NOT EXISTS
                FOR (a:User) REQUIRE a.id IS UNIQUE """)

    @classmethod
    async def init(cls):
        try:
            cls.driver = AsyncGraphDatabase.driver(uri=cls.URI, auth=cls.AUTH, database=cls.DATABASE)
            if not cls.createIndexes: return print("Didn't try to createIndex")
            async with cls.session() as session:
                await cls.create_constraints(session)
                await cls.create_indexes(session)
        except Exception as e:
            print("ERROR", e)

    @classmethod
    async def close(cls):
        await cls.driver.close()

    @classmethod
    @asynccontextmanager
    async def session(cls) -> AsyncSession:
        session = cls.driver.session(database=cls.DATABASE)
        try:
            yield session
        finally:
            await session.close()


async def db_session():
    with Database.session() as s:
        yield s
