from pytest import fixture
from sqlalchemy import create_engine
from core import settings
from db import metadata


engine = create_engine(
    url=settings.SQLITE_TEST_URL,
    connect_args={
        "check_same_thread": False,
    },
)


@fixture(autouse=True, scope="session")
def create_test_database():
    """Basic SetUp and TearDown for Clearing DataBase"""

    metadata.create_all(bind=engine)
    yield
    metadata.drop_all(bind=engine)
