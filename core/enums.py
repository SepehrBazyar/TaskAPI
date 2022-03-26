from enum import Enum
from typing import Optional


class BaseEnum(str, Enum):
    """Abstract Base Enumerate Class to Implement Shared Method Utilities"""

    @classmethod
    def get_by_value(cls, value: str) -> Optional[Enum]:
        """Get Value String & Returned Enum if Exists with this Value Else None"""

        return cls._value2member_map_.get(value)


class Level(BaseEnum):
    """Enumerate Class Levels of User Admin or Employee Types"""

    STAFF = "1"
    ADMIN = "2"


class Role(BaseEnum):
    """Enumerate Class Roles of Member Postions in Teams"""

    EMPLOYEE = "1"
    MANAGER = "2"
    OWNER = "3"
