import ormar
from fastapi import Depends, Request, HTTPException, status
from abc import ABC
from core import ItemsPerPage, DBPagination
from models import User
from .deps import get_current_user


class BaseAPIView(ABC):
    """Abstract Base View Class to Shared Dependencies etc Authentication"""

    # Shared Dependencies As a Class Atrribiutes Access from Self Parameter
    current_user: User = Depends(get_current_user, use_cache=True)


class ListCreateAPIView(BaseAPIView):
    """Class Based View for List & Create Operations for Entity Models"""

    path: str = "/"
    model: ormar.Model

    async def list(
        self,
        request: Request,
        pagination: ItemsPerPage = Depends(),
    ) -> model.Schema.List:
        """Returned the List of Entity Model with Brief Details in Pagination Mode"""

        count: int = await self.model.objects.count()
        paginate = DBPagination(url=request.url, total=count, paginations=pagination)
        if not await paginate.is_valid_page():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page Not Found."
            )

        next, previous = await paginate.next_and_previous()
        return {
            "count": count,
            "next": next,
            "previous": previous,
            "results": await self.model.objects.all(),
        }
