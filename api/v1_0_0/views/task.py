from fastapi import Request, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from core import (
    Level,
    ItemsPerPage,
    PrimaryKeySchema,
    SuccessfullSchema,
)
from models import Task, User, Project
from schemas import (
    TaskListSchema,
    TaskInDBSchema,
    TaskOutDBSchema,
    TaskUpdateSchema,
)
from decorators import check_user_level
from ..deps import BaseAPIView, get_task


router = InferringRouter()


class TaskAPIView(BaseAPIView):
    """Basic Class Based View for CRUD Operations for Task Entity Model"""

    model, router = Task, router
    name = model.get_name(lower=True)

    async def get_queryset(self, **kwargs):
        result = await super().get_queryset(**kwargs)
        return result.select_related([self.model.user, self.model.project])


@cbv(router)
class TaskListCreateAPIView(TaskAPIView):
    """Class Based View for List & Create Operations for Task Model"""

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
    ) -> TaskListSchema:
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
    async def create(self, task_form: TaskInDBSchema) -> PrimaryKeySchema:
        """Created New Project Model & Returned Primary Key UUID"""

        user = await User.objects.get_or_none(id=task_form.user_id)
        project = await Project.objects.get_or_none(id=task_form.project_id)
        if user is not None and project is not None:
            try:
                task = await Task.objects.create(
                    user=user,
                    project=project,
                    **task_form.dict(exclude={"user_id", "project_id"})
                )
            except Exception:
                detail = "Failed to Create Project."
            else:
                return project

        else:
            detail = "This User or Project does not Exist."

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


@cbv(router)
class TaskRetrieveUpdateDestroyAPIView(TaskAPIView):
    """Class Based View for Retrieve Update Destroy Operations for Task Model"""

    __PATH = "/{task_id}/"

    task: Task = Depends(get_task)

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def retrieve(self) -> TaskOutDBSchema:
        """Retrieve the Task Information Details by Get Primary Key ID in Path"""

        return self.task


    @router.patch(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def partial_update(self, fields: TaskUpdateSchema) -> SuccessfullSchema:
        """Updated the Task Information Detail with ID Primary Key in Path URL"""

        try:
            await self.task.update(**fields.dict(exclude_unset=True))
        except Exception:
            detail = "Update Data Failed."
        else:
            return SuccessfullSchema()

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


    @router.delete(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def destroy(self) -> SuccessfullSchema:
        """Delete the Task Model from Database Table with Input ID in Path URL"""

        await self.task.delete()
        return SuccessfullSchema()
