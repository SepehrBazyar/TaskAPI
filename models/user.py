import ormar
from pydantic import EmailStr
from uuid import UUID, uuid4
from typing import Optional
from core import Level, jwt_auth, MOBILE_PATTERN
from db import MainMeta

class User(ormar.Model):
    """User Model Class to Implement Method for Operations of User Entity"""

    id: UUID = ormar.UUID(uuid_format="string", primary_key=True, default=uuid4)
    mobile: str = ormar.String(unique=True, index=True, max_length=10, pattern=MOBILE_PATTERN)
    password: str = ormar.String(max_length=128)
    level: str = ormar.String(max_length=1, choices=list(Level))
    email: Optional[EmailStr] = ormar.String(max_length=255, nullable=True, default=None)
    avatar: Optional[str] = ormar.String(max_length=255, nullable=True, default=None)
    fullname: Optional[str] = ormar.String(max_length=64, nullable=True, default=None)
    is_active: bool = ormar.Boolean(index=True, default=True)

    class Meta(MainMeta):
        pass
