import orm
from uuid import uuid4
from datetime import datetime
from core import LowerNameMixin
from db import models
from .user import User
from .team import Team
from .project import Project
from .task import Task


class Work(LowerNameMixin, orm.Model):
    """Work Model Class to Implement Method for Operations of Work Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "start_time": orm.DateTime(default=datetime.today),
        "end_time": orm.DateTime(allow_null=True, default=None),
        "user_id": orm.ForeignKey(to=User, on_delete=orm.CASCADE),
        "team_id": orm.ForeignKey(to=Team, on_delete=orm.CASCADE),
        "project_id": orm.ForeignKey(to=Project, on_delete=orm.CASCADE),
        "task_id": orm.ForeignKey(to=Task, on_delete=orm.CASCADE),
    }
