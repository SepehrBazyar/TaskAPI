import ormar
from core import PrimaryKeyMixin, BaseModelSerializer
from db import MainMeta
from schemas import (
    TeamListSchema,
    TeamInDBSchema,
    TeamOutDBSchema,
    TeamUpdateSchema,
)
from .user import User
from .member import TeamUser


class Team(PrimaryKeyMixin, ormar.Model):
    """Team Model Class to Implement Method for Operations of Team Entity"""

    name: str = ormar.String(unique=True, max_length=64)
    creator: User = ormar.ForeignKey(to=User, skip_reverse=True, related_name="+")
    members = ormar.ManyToMany(
        to=User,
        through=TeamUser,
        through_relation_name="team_id",
        through_reverse_relation_name="user_id",
    )

    class Meta(MainMeta):
        pass


class TeamSerializer(BaseModelSerializer):
    """Serialzer Model Class for Team ORM Model Class with Schemas"""

    model = Team

    class Shcema(BaseModelSerializer.Shcema):
        List = TeamListSchema
        Create = TeamInDBSchema
        Retrieve = TeamOutDBSchema
        PartialUpdate = TeamUpdateSchema
