import ormar
from core import BaseModel, DBPagination, PrimaryKeyMixin
from .base import BaseGenericAPIView


class PreGenericAPIView(BaseGenericAPIView):
    """Pre Signals Generic Class Based View for CRUD Operations for an Entity Models"""

    async def pre_list(self, paginate: DBPagination, **kwargs) -> ormar.QuerySet:
        """Coroutine Method Called Before List ORM Model to Override Generics"""

        return (
            self.model.objects.filter(**kwargs)
            .offset(paginate.skip).limit(paginate.size)
        )

    async def pre_create(self, model_form: BaseModel) -> PrimaryKeyMixin:
        """Coroutine Method Called Before Create ORM Model to Override Generics"""

        return await self.model.objects.create(**model_form.dict())

    async def pre_retrieve(self, model_object: ormar.Model) -> ormar.Model:
        """Coroutine Method Called Before Retrieve ORM Model to Override Generics"""

        return model_object

    async def pre_update(self, model_object: ormar.Model, model_form: BaseModel):
        """Coroutine Method Called Before Update ORM Model to Override Generics"""

        await model_object.update(**model_form.dict(exclude_unset=True))

    async def pre_destroy(self, model_object: ormar.Model):
        """Coroutine Method Called Before Destroy ORM Model to Override Generics"""

        await model_object.delete()
