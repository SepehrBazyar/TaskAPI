from fastapi import Depends
from abc import ABC
from models import User
from .deps import get_current_user


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    current_user: User = Depends(get_current_user, use_cache=True)
