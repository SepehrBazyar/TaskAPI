import orm
from uuid import uuid4
from core import Role, LowerNameMixin
from db import models
from .user import User
from .team import Team


class Member(LowerNameMixin, orm.Model):
    """Member Model Class to Implement Method for Operations of Member Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "user_id": orm.ForeignKey(to=User, on_delete=orm.CASCADE),
        "team_id": orm.ForeignKey(to=Team, on_delete=orm.CASCADE),
        "role": orm.Enum(enum=Role, default=Role.EMPLOYEE),
        "joined_at": orm.Date(auto_now_add=True),
    }
