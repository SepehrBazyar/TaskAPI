import orm
from uuid import uuid4
from core import LowerNameMixin
from db import models
from .user import User


class Team(LowerNameMixin, orm.Model):
    """Team Model Class to Implement Method for Operations of Team Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "name": orm.String(max_length=64, unique=True),
        "creator_id": orm.ForeignKey(to=User, on_delete=orm.CASCADE),
    }
