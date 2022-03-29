import ormar
from fastapi import Request, HTTPException, status
from core import BaseModel, ItemsPerPage, DBPagination
from .signals import PreGenericAPIView


class MethodGenericAPIView(PreGenericAPIView):
    """Generic Methods Class Based View for CRUD Operations for an Entity Models"""

    async def list(
        self,
        request: Request,
        pagination: ItemsPerPage,
        params: BaseModel,
        **kwargs,
    ):
        """Returned the Brief Details List of Entity Model with Pagination"""

        items = params.dict(exclude_none=True)
        count: int = await self.model.objects.filter(**items).count()
        paginate = DBPagination(url=request.url, total=count, paginations=pagination)
        if not await paginate.is_valid_page():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page Not Found."
            )

        next, previous = await paginate.next_and_previous()
        queryset = await self.pre_list(paginate=paginate, **items)

        return {
            "count": count,
            "next": next,
            "previous": previous,
            "results": await queryset.all(),
        }

    async def create(self, new_model: BaseModel, **kwargs):
        """Create New Entity Model & Returned Primary Key UUID Response"""

        try:
            model = await self.pre_create(model_form=new_model)
        except Exception as e:
            detail: str = e.args[0] if e.args else "Insert Data Failed."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

        return {
            "id": model.id,
        }

    async def retrieve(self, model: ormar.Model, **kwargs):
        """Retrieve the Model Information Details by Get Primary Key in Path"""

        return await self.pre_retrieve(model_object=model)

    async def partial_update(
        self,
        model: ormar.Model,
        fields: BaseModel,
        **kwargs,
    ) -> bool:
        """Partial Updated the Model Fields with ID Primary Key in Path URL"""

        try:
            await self.pre_update(model_object=model, model_form=fields)
        except Exception as e:
            detail: str = e.args[0] if e.args else "Update Data Failed."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

        return True

    async def destroy(self, model: ormar.Model, **kwargs) -> bool:
        """Delete the Model from Database Table with Primary Key in Path URL"""

        await self.pre_destroy(model_object=model)
        return True
