import ormar
from typing import Optional, List
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

    async def members_list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        *args: str,
        **kwargs,
    ) -> List[TeamUser]:
        """Returned a List Contains of TeamUser Members Joined to User Table Row"""

        queryset = TeamUser.objects.filter(team=self, **kwargs)
        if args:
            queryset = queryset.order_by(args)

        if offset is not None:
            queryset = queryset.offset(offset=offset)

        if limit is not None:
            queryset = queryset.limit(limit_count=limit)

        return await queryset.select_related(TeamUser.user).all()

    class Meta(MainMeta):
        pass
