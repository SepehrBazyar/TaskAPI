from ormar import QuerySet
from core import BaseModel, DBPagination, PrimaryKeyMixin
from .base import BaseGenericAPIView


class PreGenericAPIView(BaseGenericAPIView):
    """Pre Signals Generic Class Based View for CRUD Operations for an Entity Models"""

    async def pre_list(self, paginate: DBPagination, **kwargs) -> QuerySet:
        """Coroutine Method Called Before List ORM Model to Override Generics"""

        return (
            self.model.objects.filter(**kwargs)
            .offset(paginate.skip).limit(paginate.size)
        )

    async def pre_create(self, model_form: BaseModel) -> PrimaryKeyMixin:
        """Coroutine Method Called Before Create ORM Model to Override Generics"""

        return await self.model.objects.create(**model_form.dict())
