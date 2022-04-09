from httpx import AsyncClient
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from asyncio import get_event_loop
from typing import Dict, Generator
from core import settings, Level
from db import metadata
from models import User
from schemas import UserInDBSchema
from main import app


engine: AsyncEngine = create_async_engine(settings.SQLITE_TEST_URL, echo=True)

FIRST_ADMIN = {
    "username": "9928917653",
    "password": "sepehrbazyar",
}

VERSIONS = {
    "1.0.0": "/v1.0.0/",
}


async def insert_first_admin():
    """Inserting First Admin User to Access Protected Routes View"""

    form = UserInDBSchema(
        level=Level.ADMIN,
        mobile=FIRST_ADMIN.get("username"),
        password=FIRST_ADMIN.get("password"),
    )
    await User.sign_up(form=form)


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
        await insert_first_admin()
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


@fixture(scope="session")
async def admin_token_headers(client: AsyncClient) -> Dict[str, str]:
    """PASS"""

    await insert_first_admin()
    response = await client.post(f"/user/login/", data=FIRST_ADMIN)
    tokens: Dict[str, str] = response.json()
    return {
        "Authorization": f"Bearer {tokens.get('access_token')}",
    }


@fixture(autouse=True, scope="session")
def event_loop():
    """Override the Event Loop Tests for Set Async Fixture Tests"""

    loop = get_event_loop()
    yield loop
    loop.close()
