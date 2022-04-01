from fastapi import HTTPException, status
from functools import wraps
from typing import Callable
from core import Level
from models import User


DETAIL = "Permission Denied."


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

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=DETAIL)

        return wrapper

    return decorator
