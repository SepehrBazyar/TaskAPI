from fastapi import HTTPException, status
from functools import wraps
from typing import Callable
from core import Level, Role
from models import (
    User,
    Team,
    TeamUser,
)


def check_user_level(*levels: Level):
    """Check Level of the Current User if not in Levels Raised HTTPException"""

    def decorator(function: Callable):

        @wraps(function)
        async def wrapper(*args, **kwargs):
            self = kwargs.get("self")
            try:
                current_user: User = getattr(self, "current_user")
            except AttributeError:
                pass
            else:
                if current_user.level_ in levels:
                    return await function(*args, **kwargs)

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied."
            )

        return wrapper

    return decorator


def check_member_role_team(*roles: Role):
    """Check Team Role of the Current User if not in Roles Raised HTTPException"""

    def decorator(function: Callable):

        @wraps(function)
        async def wrapper(*args, **kwargs):
            self = kwargs.get("self")
            try:
                current_user: User = getattr(self, "current_user")
                team: Team = getattr(self, "team")
            except AttributeError:
                pass
            else:
                member = await TeamUser.objects.get(user=current_user, team=team)
                if member.role_ in roles:
                    return await function(*args, **kwargs)

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied."
            )

        return wrapper

    return decorator
