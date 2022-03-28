from fastapi_utils.inferring_router import InferringRouter
from models import UserSerializer
from api.base import GenericAPIView


router = InferringRouter()


generic = GenericAPIView(router, serializer=UserSerializer)
generic.list_create()
