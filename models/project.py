import orm
from uuid import uuid4
from core import LowerNameMixin
from db import models
from .team import Team


class Project(LowerNameMixin, orm.Model):
    """Project Model Class to Implement Method for Operations of Project Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "name": orm.String(max_length=64, unique=True),
        "description": orm.Text(allow_null=True, default=None),
        "start_date": orm.Date(allow_null=True, default=None),
        "end_date": orm.Date(allow_null=True, default=None),
        "team_id": orm.ForeignKey(to=Team, on_delete=orm.CASCADE),
    }
