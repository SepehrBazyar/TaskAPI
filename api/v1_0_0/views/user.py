from fastapi_utils.inferring_router import InferringRouter
from models import User
from api.base import GenericAPIView


router = InferringRouter()


generic = GenericAPIView(User, User.Shcema, router)
generic.list_create()
