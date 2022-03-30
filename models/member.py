import ormar
from datetime import date
from core import Role, PrimaryKeyMixin
from db import MainMeta
from schemas import (
    MemberListSchema,
    MemberInDBSchema,
    MemberOutDBSchema,
    MemberUpdateSchema,
)


class TeamUser(PrimaryKeyMixin, ormar.Model):
    """User Team Model Class to Implement Method for Operations of Member Entity"""

    role: str = ormar.String(max_length=1, choices=list(Role), default=Role.EMPLOYEE.value)
    joined_at: date = ormar.Date(default=date.today)

    user_id = ormar.UUID(uuid_format="string")
    team_id = ormar.UUID(uuid_format="string")

    @ormar.property_field
    def role_(self) -> Role:
        """Returned the Role Instance of Class Model by Role Value in Database"""

        return Role.get_by_value(value=self.role)

    class Meta(MainMeta):
        tablename = "members"
        constraints = [
            ormar.UniqueColumns("user_id", "team_id"),
        ]

    class Shcema:
        """Inner Class for Contain Collection of Shcemas Use in Routes"""

        List = MemberListSchema
        Create = MemberInDBSchema
        Retrieve = MemberOutDBSchema
        PartialUpdate = MemberUpdateSchema
