import ormar
from uuid import UUID, uuid4
from db import MainMeta
from schemas import (
    TeamListSchema,
    TeamInDBSchema,
    TeamOutDBSchema,
    TeamUpdateSchema,
)
from .user import User
from .member import UserTeam


class Team(ormar.Model):
    """Team Model Class to Implement Method for Operations of Team Entity"""

    id: UUID = ormar.UUID(uuid_format="string", primary_key=True, default=uuid4)
    name: str = ormar.String(unique=True, max_length=64)
    members = ormar.ManyToMany(to=User, through=UserTeam)

    class Meta(MainMeta):
        pass

    class Shcema:
        """Inner Class for Contain Collection of Shcemas Use in Routes"""

        List = TeamListSchema
        Create = TeamInDBSchema
        Retrieve = TeamOutDBSchema
        PartialUpdate = TeamUpdateSchema
