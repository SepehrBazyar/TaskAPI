from fastapi_utils.inferring_router import InferringRouter
from core import Level
from models import Team, TeamSerializer
from decorators import check_user_level
from generics import GenericAPIView


router = InferringRouter()


class TeamGenericAPIView(GenericAPIView):
    """Generic Class Based Views for Team Model Override Some of Methods"""

    pass


generic = TeamGenericAPIView(router, serializer=TeamSerializer)
generic.list_create()
generic.retrieve_update_destory()
