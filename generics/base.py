from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from abc import ABC
from typing import Optional
from core import BaseModelSerializer
from models import User
from .deps import get_current_user


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    current_user: User = Depends(get_current_user, use_cache=True)


class BaseGenericAPIView(ABC):
    """Basic Generic Class Based View for CRUD Operations for an Entity Models"""

    def __init__(
        self,
        router: InferringRouter,
        serializer: BaseModelSerializer,
        name: Optional[str] = None,
    ):
        self.router = router
        self.model, self.schemas = serializer.model, serializer.Shcema
        self.name = self.model.get_name(lower=True) if name is None else name
