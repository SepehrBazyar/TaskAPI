import orm
from uuid import uuid4
from core import Level, LowerNameMixin, MOBILE_PATTERN
from db import models


class User(LowerNameMixin, orm.Model):
    """User Model Class to Implement Method for Operations of User Entity"""

    registry = models
    fields = {
        "id": orm.UUID(primary_key=True, default=uuid4),
        "mobile": orm.String(unique=True, index=True, pattern=MOBILE_PATTERN),
        "password": orm.String(max_length=128),
        "level": orm.Enum(Level, default=Level.EMPLOYEE),
        "email": orm.Email(allow_null=True, default=None),
        "avatar": orm.Text(allow_null=True, default=None),
        "fullname": orm.String(max_length=64, allow_null=True, default=None),
        "is_active": orm.Boolean(index=True, default=True),
    }
