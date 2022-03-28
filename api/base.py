import ormar
from fastapi import Depends, Request, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from abc import ABC
from typing import Optional
from core import (
    BaseModel,
    ItemsPerPage,
    DBPagination,
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
        try:
            model: ormar.Model = await self.model.objects.create(**new_model.dict())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insert Data Failed."
            )

        return {
            "id": model.id,
        }

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
