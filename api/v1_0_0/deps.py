from fastapi import Depends, HTTPException, status
from abc import ABC
from core import oauth2_schema, jwt_auth
from models import User


async def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    """Authentication Dependency to Returned Current User Data Else Unauthorize"""

    user_id = await jwt_auth.get_user_id(access_token=token)
    if user_id is not None:
        user = await User.objects.get_or_none(id=user_id)
        if user is not None:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    current_user: User = Depends(get_current_user, use_cache=True)
