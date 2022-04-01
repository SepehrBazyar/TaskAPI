import ormar
from datetime import date
from typing import Optional
from core import PrimaryKeyMixin
from db import MainMeta
from .user import User
from .project import Project


class Task(PrimaryKeyMixin, ormar.Model):
    """Task Model Class to Implement Method for Operations of Task Entity"""

    name: str = ormar.String(max_length=64, nullalbe=False)
    description: Optional[str] = ormar.Text(nullable=True, default=None)
    start_date: Optional[date] = ormar.Date(nullable=True, default=None)
    end_date: Optional[date] = ormar.Date(nullable=True, default=None)
    is_halted: bool = ormar.Boolean(index=True, nullable=False, default=True)
    user: User = ormar.ForeignKey(to=User)
    project: Project = ormar.ForeignKey(to=Project)

    class Meta(MainMeta):
        orders_by = ["-end_date", "-start_date"]
        constraints = [
            ormar.UniqueColumns("user", "project", "name"),
        ]
