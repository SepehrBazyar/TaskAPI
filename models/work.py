import ormar
from datetime import datetime
from core import PrimaryKeyMixin
from db import MainMeta
from .user import User
from .team import Team
from .project import Project
from .task import Task


class Work(PrimaryKeyMixin, ormar.Model):
    """Work Model Class to Implement Method for Operations of Work Entity"""

    start_time: datetime = ormar.DateTime(nullable=False, default=datetime.today)
    end_time: datetime = ormar.DateTime(nullable=True, default=None)
    user: User = ormar.ForeignKey(to=User)
    team: Team = ormar.ForeignKey(to=Team)
    project: Project = ormar.ForeignKey(to=Project)
    task: Task = ormar.ForeignKey(to=Task)

    class Meta(MainMeta):
        pass
