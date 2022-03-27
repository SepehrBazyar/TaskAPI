from fastapi_utils.inferring_router import InferringRouter
from models import User
from api.base import ListCreateAPIView, Generics


router = InferringRouter()

class UserListCreateAPIView(ListCreateAPIView):
    """PASS"""

    model = User


generic = Generics(router, model=User)
generic.list_create()
