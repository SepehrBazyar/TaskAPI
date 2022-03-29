from core import BaseModel, PrimaryKeyMixin
from .base import BaseGenericAPIView


class PreGenericAPIView(BaseGenericAPIView):
    """Pre Signals Generic Class Based View for CRUD Operations for an Entity Models"""

    async def perform_create(self, model_form: BaseModel) -> PrimaryKeyMixin:
        """Coroutine Method Called Before Create ORM Model to Override Generics"""

        return await self.model.objects.create(**model_form.dict())
