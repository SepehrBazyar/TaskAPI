import orm
from uuid import uuid4
from core import LowerNameMixin
from db import models


class User(LowerNameMixin, orm.Model):
    """User Model Class to Implement Method for Operations of User Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "username": orm.String(unique=True, index=True, min_length=4, max_length=32),
    }
