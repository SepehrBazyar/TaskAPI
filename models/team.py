import ormar
from typing import Optional
from core import Role, PrimaryKeyMixin
from db import MainMeta
from schemas import TeamInDBSchema
from .user import User
from .member import TeamUser


class Team(PrimaryKeyMixin, ormar.Model):
    """Team Model Class to Implement Method for Operations of Team Entity"""

    name: str = ormar.String(unique=True, max_length=64)
    creator: User = ormar.ForeignKey(to=User, skip_reverse=True, related_name="+")
    members = ormar.ManyToMany(
        to=User,
        through=TeamUser,
        related_name="member",
        through_relation_name="team",
        through_reverse_relation_name="user",
    )

    @classmethod
    async def found(cls, creator: User, form: TeamInDBSchema) -> Optional["Team"]:
        """Found method to Create New Team with User Owner in Members List"""

        if not await cls.objects.filter(name=form.name).exists():
            team = await cls.objects.create(creator=creator, **form.dict())
            await team.members.add(creator, role=Role.OWNER)
            return team

    class Meta(MainMeta):
        pass
