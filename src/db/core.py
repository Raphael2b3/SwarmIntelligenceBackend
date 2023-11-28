import os
from contextlib import asynccontextmanager
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession

import load_env


class Index:
    tagsFullText = "TagsFulltext"
    statementsFullText = "StatementsFulltext"


driver: AsyncDriver
env: dict


def init():
    global driver, env
    env = load_env.load_settings_from_env("DB_CONNECTION_STRING", "DB_USERNAME", "DB_PASSWORD", "DB_DATABASE")
    driver = AsyncGraphDatabase.driver(uri=env["DB_CONNECTION_STRING"],
                                       auth=(env["DB_USERNAME"], env["DB_PASSWORD"]),
                                       database=env["DB_DATABASE"])


@asynccontextmanager
async def session() -> AsyncSession:
    _session = driver.session(database=env["DB_DATABASE"])
    try:
        yield _session
    finally:
        await _session.close()


def transaction(func):
    async def transaction_with_session(**kwargs):
        async with session() as se:
            return await se.execute_write(func, **kwargs)

    return transaction_with_session


async def close():
    await driver.close()
