import ormar
from uuid import UUID, uuid4
from datetime import date
from core import Role
from db import MainMeta
from schemas import (
    MemberListSchema,
    MemberInDBSchema,
    MemberOutDBSchema,
    MemberUpdateSchema,
)


class UserTeam(ormar.Model):
    """User Team Model Class to Implement Method for Operations of Member Entity"""

    id: UUID = ormar.UUID(uuid_format="string", primary_key=True, default=uuid4)
    role: str = ormar.String(max_length=1, choices=list(Role), default=Role.EMPLOYEE.value)
    joined_at: date = ormar.Date(default=date.today)

    @ormar.property_field
    def role_(self) -> Role:
        """Returned the Role Instance of Class Model by Role Value in Database"""

        return Role.get_by_value(value=self.role)

    class Meta(MainMeta):
        tablename = "members"
        # constraints = [
        #     ormar.UniqueColumns("user", "team"),
        # ]

    class Shcema:
        """Inner Class for Contain Collection of Shcemas Use in Routes"""

        List = MemberListSchema
        Create = MemberInDBSchema
        Retrieve = MemberOutDBSchema
        PartialUpdate = MemberUpdateSchema
