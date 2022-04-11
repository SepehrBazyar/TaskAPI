from ormar import ModelMeta
from databases import Database
from sqlalchemy import MetaData
from uvicorn.config import logger
from core import settings


metadata = MetaData()
if not settings.TESTING:
    DB_NAME = "PostgreSQL"
    database = Database(url=settings.POSTGRESQL_URL)
else:
    DB_NAME = "SQLite"
    database = Database(url=settings.SQLITE_TEST_URL, force_rollback=True)


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
        logger.error(f"{DB_NAME} Connection Failed {e}.")
    else:
        logger.info(f"{DB_NAME} Connected.")


async def close_postgresql_connection():
    """Shutdown Event Handler for Disconnect to PostgreSQL Database"""

    await database.disconnect()
    logger.info(f"{DB_NAME} Closed.")
