from fastapi_utils.inferring_router import InferringRouter
from core import Level, Role
from models import Team, TeamSerializer
from decorators import check_user_level
from generics import GenericAPIView


router = InferringRouter()


class TeamGenericAPIView(GenericAPIView):
    """Generic Class Based Views for Team Model Override Some of Methods"""

    __ERROR = "Team Name Already Existed."

    @check_user_level(Level.ADMIN)
    async def list(self, request, pagination, params, **kwargs):
        return await super().list(request, pagination, params, **kwargs)

    @check_user_level(Level.ADMIN)
    async def create(self, new_model, **kwargs):
        return await super().create(new_model, **kwargs)

    async def pre_create(
        self,
        model_form: TeamSerializer.Shcema.Create,
    ) -> TeamSerializer.model:
        """Perform Create Method Called Before Create & Use Found Team Method"""

        new_team = await TeamSerializer.model.found(form=model_form)
        if new_team is not None:
            return new_team

        raise ValueError(self.__ERROR)


generic = TeamGenericAPIView(router, serializer=TeamSerializer)
generic.list_create()
