from orm import ModelRegistry
from databases import Database
from uvicorn.config import logger
from core import settings


database = Database(settings.POSTGRESQL_URL)
models = ModelRegistry(database=database)


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
