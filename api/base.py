import ormar
from fastapi import Depends, Request, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from abc import ABC
from typing import Optional, List
from core import ItemsPerPage, DBPagination, BaseModelSerializer
from models import User
from .deps import get_current_user


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    # current_user: User = Depends(get_current_user, use_cache=True)


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

    async def list(
        self,
        request: Request,
        pagination: ItemsPerPage,
    ):
        count: int = await self.model.objects.count()
        paginate = DBPagination(url=request.url, total=count, paginations=pagination)
        if not await paginate.is_valid_page():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page Not Found."
            )

        next, previous = await paginate.next_and_previous()
        models: List[ormar.Model] = (
            await self.model.objects.offset(paginate.skip).limit(paginate.size).all()
        )

        return {
            "count": count,
            "next": next,
            "previous": previous,
            "results": models,
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
            ) -> __parent.schemas.List:
                """Returned the List of Entity Model with Brief Details in Pagination Mode"""

                return await self.__parent.list(request=request, pagination=pagination)
