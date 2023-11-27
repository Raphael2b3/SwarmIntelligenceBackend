from contextlib import asynccontextmanager
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
import settings

driver: AsyncDriver
initialized = False


def init(*, uri, auth, database):
    global driver, initialized
    settings.pass_settings(uri=uri, auth=auth, database=database)
    driver = AsyncGraphDatabase.driver(uri=settings.URI, auth=settings.AUTH, database=settings.DATABASE)
    initialized = True


@asynccontextmanager
async def session() -> AsyncSession:
    _session = driver.session(database=settings.DATABASE)
    try:
        yield _session
    finally:
        await _session.close()


async def transaction(func):
    async def wrapper(**kwargs):
        async with session() as se:
            return se.execute_write(func, **kwargs)

    return wrapper


async def close():
    global initialized
    initialized = False
    await driver.close()
