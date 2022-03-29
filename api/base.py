import ormar
from fastapi import Depends, Request, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from uuid import UUID
from abc import ABC
from typing import Optional
from core import (
    BaseModel,
    ItemsPerPage,
    DBPagination,
    PrimaryKeyMixin,
    PrimaryKeySchema,
    BaseModelSerializer,
)
from models import User
from .deps import get_current_user


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    current_user: User = Depends(get_current_user, use_cache=True)


class GenericAPIView:
    """Generic Class Based View for CRUD Operations for an Entity Models"""

    def __init__(
        self,
        router: InferringRouter,
        serializer: BaseModelSerializer,
        name: Optional[str] = None,
    ):
        self.router = router
        self.model, self.schemas = serializer.model, serializer.Shcema
        self.name = self.model.get_name(lower=True) if name is None else name

    async def list(self, request: Request, pagination: ItemsPerPage, params: BaseModel):
        """Returned the Brief Details List of Entity Model with Pagination"""

        items = params.dict(exclude_none=True)
        count: int = await self.model.objects.filter(**items).count()
        paginate = DBPagination(url=request.url, total=count, paginations=pagination)
        if not await paginate.is_valid_page():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page Not Found."
            )

        next, previous = await paginate.next_and_previous()
        queryset: ormar.QuerySet = (
            self.model.objects.filter(**items).offset(paginate.skip).limit(paginate.size)
        )

        return {
            "count": count,
            "next": next,
            "previous": previous,
            "results": await queryset.all(),
        }

    async def create(self, new_model: BaseModel):
        """Create New Entity Model & Returned Primary Key UUID Response"""

        try:
            model = await self.perform_create(model_form=new_model)
        except Exception as e:
            detail: str = e.args[0] if e.args else "Insert Data Failed."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

        return {
            "id": model.id,
        }
    
    async def retrieve(self, model: ormar.Model):
        """Retrieve the Model Information Details by Get Primary Key in Path"""

        return model

    async def dependency(self, id: UUID) -> ormar.Model:
        """Dependency to Get Model ID in Path URL & Returned Model Object if Exists"""

        model: Optional[ormar.Model] = await self.model.objects.get_or_none(id=id)
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.name.title()} Not Found.",
            )

        return model

    async def perform_create(self, model_form: BaseModel) -> PrimaryKeyMixin:
        """Coroutine Method Called Before Create ORM Model to Override Generics"""

        return await self.model.objects.create(**model_form.dict())

    def list_create(self, path: str = "/"):
        """Generate Class Based View for List & Create API View Operations"""

        @cbv(self.router)
        class ListCreateAPIView(BaseAPIView):
            """Class Based View for List & Create Operations for Entity Models"""

            __parent = self

            @__parent.router.get(
                path,
                status_code=status.HTTP_200_OK,
            )
            async def list(
                self,
                request: Request,
                pagination: ItemsPerPage = Depends(),
                params: __parent.schemas.Filter = Depends(),
            ) -> __parent.schemas.List:
                """Returned the Brief Details List of Entity Model with Pagination"""

                return await self.__parent.list(
                    request=request, pagination=pagination, params=params
                )

            @__parent.router.post(
                path,
                status_code=status.HTTP_201_CREATED,
            )
            async def create(
                self, new_model: __parent.schemas.Create
            ) -> PrimaryKeySchema:
                """Create New Entity Model & Returned Primary Key UUID Response"""

                return await self.__parent.create(new_model=new_model)

    def retrieve_update_destory(self, path: str = "/{id}/"):
        """Generate Class Based View for List & Create API View Operations"""

        @cbv(self.router)
        class RetrieveUpdateDestroyAPIView(BaseAPIView):
            """Class Based View Retrieve Update Destroy Operations for a Single Model"""

            __parent = self
            object: ormar.Model = Depends(self.dependency)

            @__parent.router.get(
                path,
                status_code=status.HTTP_200_OK,
            )
            async def retrieve(self) -> __parent.schemas.Retrieve:
                """Retrieve the Model Information Details by Get Primary Key in Path"""

                return await self.__parent.retrieve(model=self.object)
