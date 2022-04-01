from fastapi import Request, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from core import (
    Level,
    ItemsPerPage,
    PrimaryKeySchema,
    SuccessfullSchema,
)
from models import Project, Team
from schemas import (
    ProjectListSchema,
    ProjectInDBSchema,
    ProjectOutDBSchema,
    ProjectUpdateSchema,
)
from decorators import check_user_level
from ..deps import BaseAPIView, get_project


router = InferringRouter()


class ProjectAPIView(BaseAPIView):
    """Basic Class Based View for CRUD Operations for Project Entity Model"""

    model, router = Project, router
    name = model.get_name(lower=True)

    async def get_queryset(self, **kwargs):
        result = await super().get_queryset(**kwargs)
        return result.select_related(self.model.team)


@cbv(router)
class ProjectListCreateAPIView(ProjectAPIView):
    """Class Based View for List & Create Operations for Project Model"""

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
    ) -> ProjectListSchema:
        """Returned the List of Project with Brief Details in Pagination Mode"""

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
    async def create(self, project_form: ProjectInDBSchema) -> PrimaryKeySchema:
        """Created New Project Model & Returned Primary Key UUID"""

        team = await Team.objects.get_or_none(id=project_form.team_id)
        if team is not None:
            try:
                project = await Project.objects.create(
                    team=team, **project_form.dict(exclude={"team_id"})
                )
            except Exception:
                detail = "Failed to Create Project."
            else:
                return project

        else:
            detail = "This Team does not Exist."

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
