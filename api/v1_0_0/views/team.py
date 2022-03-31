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
from models import User, Team, TeamUser
from schemas import (
    TeamListSchema,
    TeamInDBSchema,
    TeamOutDBSchema,
    TeamUpdateSchema,
    MemberListSchema,
    MemberInDBSchema,
    MemberOutDBSchema,
    MemberUpdateSchema,
    MemberFilterSchema,
)
from decorators import (
    check_user_level,
    check_member_role_team,
    check_member_role_access,
)
from ..deps import (
    get_team,
    get_member,
    BaseAPIView,
)


router = InferringRouter()


class TeamAPIView(BaseAPIView):
    """Basic Class Based View for CRUD Operations for Team Entity Model"""

    model, router = Team, router
    name = model.get_name(lower=True)


@cbv(router)
class TeamListCreateAPIView(TeamAPIView):
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
class TeamRetrieveUpdateDestroyAPIView(TeamAPIView):
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


class MemberAPIView(TeamAPIView):
    """Basic Class Based View for CRUD Operations for Team Entity Model"""

    model = TeamUser

    async def get_queryset(self, **kwargs):
        result = await super().get_queryset(**kwargs)
        return result.select_related(self.model.user)


@cbv(router)
class MemberListCreateAPIView(MemberAPIView):
    """Class Based View for List & Create Operations for Team Model"""

    __PATH = "/{team_id}/member/"

    team: Team = Depends(get_team)

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_member_role_team(Role.OWNER, Role.MANAGER)
    async def list(
        self,
        request: Request,
        pagination: ItemsPerPage = Depends(),
        params: MemberFilterSchema = Depends(),
    ) -> MemberListSchema:
        """Returned the List of Team with Brief Details in Pagination Mode"""

        count, next, previous, queryset = await self.get_list(
            url=request.url,
            pagination=pagination,
            team=self.team,
            **params.dict(exclude_none=True),
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
    @check_member_role_team(Role.OWNER, Role.MANAGER)
    async def create(self, member_form: MemberInDBSchema) -> SuccessfullSchema:
        """Added New Member Model to a Team Entity & Returned Primary Key UUID"""

        user = await User.objects.get_or_none(id=member_form.user_id)
        if user is not None:
            try:
                await self.team.members.add(
                    item=user,
                    **member_form.dict(exclude={"user_id"}),
                )
            except Exception:
                detail = "Failed to Add Member."
            else:
                return SuccessfullSchema()

        else:
            detail = "This User does not Exist."

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


@cbv(router)
class MemberRetrieveUpdateDestroyAPIView(MemberAPIView):
    """Class Based View for Retrieve Update Destroy Operations for Member Model"""

    __PATH = "/{team_id}/member/{user_id}/"

    member: TeamUser = Depends(get_member)

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_member_role_access
    async def retrieve(self) -> MemberOutDBSchema:
        """Retrieve the Member Information Details by Get Primary Key ID in Path"""

        return self.member


    @router.delete(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_member_role_access
    async def destroy(self) -> SuccessfullSchema:
        """Remove the Member Models from Members of this Team Many to Many Relation"""

        await self.member.delete()
        return SuccessfullSchema()
