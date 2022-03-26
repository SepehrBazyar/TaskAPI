from enum import Enum


class Level(str, Enum):
    """Enumerate Class Levels of User Admin or Employee Types"""

    EMPLOYEE = "1"
    ADMIN = "2"


class Role(str, Enum):
    """Enumerate Class Roles of Member Postions in Teams"""

    EMPLOYEE = "1"
    MANAGER = "2"
    OWNER = "3"
