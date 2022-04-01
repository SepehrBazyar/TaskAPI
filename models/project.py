import ormar
from datetime import date
from typing import Optional
from core import PrimaryKeyMixin
from db import MainMeta
from .team import Team


class Project(PrimaryKeyMixin, ormar.Model):
    """Project Model Class to Implement Method for Operations of Project Entity"""

    name: str = ormar.String(max_length=64, nullalbe=False)
    description: Optional[str] = ormar.Text(nullable=True, default=None)
    start_date: Optional[date] = ormar.Date(nullable=True, default=None)
    end_date: Optional[date] = ormar.Date(nullable=True, default=None)
    team: Team = ormar.ForeignKey(to=Team)    

    class Meta(MainMeta):
        orders_by = ["-end_date", "-start_date"]
        constraints = [
            ormar.UniqueColumns("team", "name"),
        ]
