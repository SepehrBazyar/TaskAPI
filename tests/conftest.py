from httpx import AsyncClient
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from asyncio import get_event_loop
from typing import Generator
from core import settings
from db import metadata
from main import app


engine: AsyncEngine = create_async_engine(settings.SQLITE_TEST_URL, echo=True)


@fixture(autouse=True, scope="session")
async def create_test_database():
    """SetUp & TearDown Fixture to Create & Delete Database by Metadata"""

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        yield
        await conn.run_sync(metadata.drop_all)


@fixture(autouse=True, scope="function")
async def clean_tables_database():
    """Clearing Database Tables to Delete All Rows for Each Test Case"""

    try:
        yield
    finally:
        async with engine.begin() as conn:
            for table in reversed(metadata.sorted_tables):
                await conn.execute(table.delete())


@fixture(scope="session")
async def client() -> Generator[AsyncClient, None, None]:
    """Session Generator Fixture to Yielding Async Client for Requesting APIs"""

    async with AsyncClient(app=app, base_url=settings.BASE_URL) as client:
        yield client


@fixture(autouse=True, scope="session")
def event_loop():
    """Override the Event Loop Tests for Set Async Fixture Tests"""

    loop = get_event_loop()
    yield loop
    loop.close()
