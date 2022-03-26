import ormar
from uuid import UUID, uuid4
from core import Level, MOBILE_PATTERN
from db import MainMeta


class User(ormar.Model):
    """User Model Class to Implement Method for Operations of User Entity"""

    id: UUID = ormar.UUID(uuid_format="string", primary_key=True, default=uuid4)
    mobile: str = ormar.String(unique=True, index=True, max_length=10, pattern=MOBILE_PATTERN)
    password: str = ormar.String(max_length=128)

    class Meta(MainMeta):
        pass

    # fields = {
    #     "id": orm.UUID(primary_key=True, default=uuid4),
    #     "mobile": orm.String(unique=True, index=True, max_length=10, pattern=MOBILE_PATTERN),
    #     "password": orm.String(max_length=128),
    #     "level": orm.Enum(enum=Level, default=Level.EMPLOYEE),
    #     "email": orm.Email(max_length=255, allow_null=True, default=None),
    #     "avatar": orm.Text(allow_null=True, default=None),
    #     "fullname": orm.String(max_length=64, allow_null=True, default=None),
    #     "is_active": orm.Boolean(index=True, default=True),
    # }
