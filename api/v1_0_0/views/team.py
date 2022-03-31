from fastapi import Request, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from core import (
    Role,
    Level,
    ItemsPerPage,
    PrimaryKeySchema,
    SuccessfullSchema,
)
from models import Team
from schemas import (
    TeamListSchema,
    TeamInDBSchema,
    TeamOutDBSchema,
    TeamUpdateSchema,
)
from decorators import check_user_level
from ..deps import BaseAPIView, get_team


router = InferringRouter()


class TeamAPIView(BaseAPIView):
    """Basic Class Based View for CRUD Operations for Team Entity Model"""

    model, router = Team, router
    name = model.get_name(lower=True)


@cbv(router)
class UserListCreateAPIView(TeamAPIView):
    """Class Based View for List & Create Operations for Team Model"""

    __PATH = "/"

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def list(
        self,
        request: Request,
        pagination: ItemsPerPage = Depends(),
    ) -> TeamListSchema:
        """Returned the List of Team with Brief Details in Pagination Mode"""

        count, next, previous, queryset = await self.get_list(
            url=request.url, pagination=pagination
        )

        return {
            "count": count,
            "next": next,
            "previous": previous,
            "results": await queryset.all(),
        }


    @router.post(
        __PATH,
        status_code=status.HTTP_201_CREATED,
    )
    @check_user_level(Level.ADMIN)
    async def create(self, team_form: TeamInDBSchema) -> PrimaryKeySchema:
        """Founding New Team Model with Founder Method & Returned Primary Key UUID"""

        new_team = await self.model.found(form=team_form, creator=self.current_user)
        if new_team is not None:
            return new_team

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team Name Already Existed.",
        )


@cbv(router)
class UserRetrieveUpdateDestroyAPIView(TeamAPIView):
    """Class Based View for Retrieve Update Destroy Operations for User Model"""

    __PATH = "/{team_id}/"

    team: Team = Depends(get_team)

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def retrieve(self) -> TeamOutDBSchema:
        """Retrieve the Team Information Details by Get Primary Key ID in Path"""

        return self.team


    @router.patch(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def partial_update(self, fields: TeamUpdateSchema) -> SuccessfullSchema:
        """Updated the Team Information Detail with ID Primary Key in Path URL"""

        flag = await self.team.rename(update_form=fields)
        if flag:
            return SuccessfullSchema()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Update Data Failed."
        )


    @router.delete(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def destroy(self) -> SuccessfullSchema:
        """Delete the Team Model from Database Table with Input ID in Path URL"""

        await self.team.delete()
        return SuccessfullSchema()
