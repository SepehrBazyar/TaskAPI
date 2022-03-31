import ormar
from datetime import date
from core import Role, PrimaryKeyMixin
from db import MainMeta


class TeamUser(PrimaryKeyMixin, ormar.Model):
    """User Team Model Class to Implement Method for Operations of Member Entity"""

    role: str = ormar.String(max_length=1, choices=list(Role), default=Role.EMPLOYEE.value)
    joined_at: date = ormar.Date(default=date.today)

    # Foreign Keys
    user = ormar.UUID(uuid_format="string")
    team = ormar.UUID(uuid_format="string")

    @ormar.property_field
    def role_(self) -> Role:
        """Returned the Role Instance of Class Model by Role Value in Database"""

        return Role.get_by_value(value=self.role)

    class Meta(MainMeta):
        tablename = "members"
        constraints = [
            ormar.UniqueColumns("user", "team"),
        ]
