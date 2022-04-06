from ormar import ModelMeta
from databases import Database
from sqlalchemy import MetaData
from uvicorn.config import logger
from core import settings


DATABASE_URL = settings.SQLITE_TEST_URL if settings.TESTING else settings.POSTGRESQL_URL

database = Database(url=DATABASE_URL)
metadata = MetaData()


class MainMeta(ModelMeta):
    """Singleton Meta Class Metadata & Database Attrs ORM Model Classes"""

    metadata = metadata
    database = database


async def connect_to_postgresql():
    """Startup Event Handler for Connect to PostgreSQL Database"""

    await database.connect()
    try:
        await database.execute("SELECT 1")
    except Exception as e:
        logger.error(f"PostgreSQL Connection Failed {e}.")
    else:
        logger.info("PostgreSQL Connected.")


async def close_postgresql_connection():
    """Shutdown Event Handler for Disconnect to PostgreSQL Database"""

    await database.disconnect()
    logger.info("PostgreSQL Closed.")
