import orm
from uuid import uuid4
from core import LowerNameMixin
from db import models
from .member import Member
from .project import Project


class Task(LowerNameMixin, orm.Model):
    """Task Model Class to Implement Method for Operations of Task Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "name": orm.String(max_length=64, unique=True),
        "description": orm.Text(allow_null=True, default=None),
        "start_date": orm.Date(allow_null=True, default=None),
        "end_date": orm.Date(allow_null=True, default=None),
        "is_halted": orm.Boolean(index=True, default=True),
        "member_id": orm.ForeignKey(to=Member, on_delete=orm.CASCADE),
        "project_id": orm.ForeignKey(to=Project, on_delete=orm.CASCADE),
    }
