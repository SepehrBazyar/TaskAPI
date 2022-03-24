from enum import Enum


class Level(str, Enum):
    """Enumerate Class Levels of User Admin or Employee Types"""

    ADMIN = 1
    EMPLOYEE = 2


class Role(str, Enum):
    """Enumerate Class Roles of Member Postions in Teams"""

    OWNER = 1
    MANAGER = 2
    EMPLOYEE = 3
