from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from asyncio import get_event_loop
from core import settings
from db import metadata


engine: AsyncEngine = create_async_engine(settings.SQLITE_TEST_URL, echo=True)


@fixture(autouse=True, scope="session")
async def create_test_database():
    """Basic SetUp and TearDown for Clearing DataBase"""

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        yield
        await conn.run_sync(metadata.drop_all)


@fixture(autouse=True, scope="session")
def event_loop():
    """Override the Event Loop Tests for Set Async Fixture Tests"""

    loop = get_event_loop()
    yield loop
    loop.close()
