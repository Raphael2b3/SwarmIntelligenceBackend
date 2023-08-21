from contextlib import asynccontextmanager

from neo4j import AsyncGraphDatabase, AsyncDriver

from env import DB_CONNECTION_STRING, DB_PASSWORD, DB_USERNAME

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"


# TODO Create indeces
"""
INDECES: 
    Statement TEXT
    PROJECT TEXT
    Statement ID
    PROJECT ID
    CONNECTION ID?
    USERNAME 


"""


class Database:
    driver: AsyncDriver
    URI = DB_CONNECTION_STRING
    AUTH = (DB_USERNAME, DB_PASSWORD)
    DATABASE = "neo4j"

    @classmethod
    def init(cls):
        cls.driver = AsyncGraphDatabase.driver(uri=cls.URI, auth=cls.AUTH, database=cls.DATABASE)

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
