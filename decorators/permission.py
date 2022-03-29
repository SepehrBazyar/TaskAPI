from fastapi import HTTPException, status
from functools import wraps
from typing import Callable
from core import Level
from models import User


def check_user_level(*levels: Level):
    """Check Level of the Current User if not in Levels List Raised HTTPException"""

    def decorator(function: Callable):

        @wraps(function)
        async def wrapper(*args, **kwargs):
            current_user: User = getattr(kwargs.get("self"), "current_user")
            if current_user.level_ is levels:
                return await function(*args, **kwargs)

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied."
            )

        return wrapper

    return decorator
