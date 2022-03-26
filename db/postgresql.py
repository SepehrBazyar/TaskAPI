import ormar
from databases import Database
from sqlalchemy import MetaData
from uvicorn.config import logger
from uuid import UUID, uuid4
from core import settings


database = Database(settings.POSTGRESQL_URL)
metadata = MetaData()


class AbstractBaseModel(ormar.Model):
    """Basic Abstraction Model Class with Meta Intern Class & UUID PK Parameter"""

    class Meta(ormar.ModelMeta):
        abstract = True
        metadata = metadata
        database = database

    id: UUID = ormar.UUID(uuid_format="string", primary_key=True, default=uuid4)


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
