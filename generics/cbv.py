import ormar
from fastapi import Request, Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from uuid import UUID
from typing import Optional
from core import ItemsPerPage, PrimaryKeySchema, SuccessfullSchema
from .base import BaseAPIView
from .methods import MethodGenericAPIView


class GenericAPIView(MethodGenericAPIView):
    """Generic Class Based View for CRUD Operations for an Entity Models"""

    async def dependency(self, id: UUID) -> ormar.Model:
        """Dependency to Get Model ID in Path URL & Returned Model Object if Exists"""

        model: Optional[ormar.Model] = await self.model.objects.get_or_none(id=id)
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.name.title()} Not Found.",
            )

        return model

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
                    request=request,
                    pagination=pagination,
                    params=params,
                    current_user=self.current_user,
                )

            @__parent.router.post(
                path,
                status_code=status.HTTP_201_CREATED,
            )
            async def create(
                self, new_model: __parent.schemas.Create
            ) -> PrimaryKeySchema:
                """Create New Entity Model & Returned Primary Key UUID Response"""

                return await self.__parent.create(
                    new_model=new_model,
                    current_user=self.current_user,
                )

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

                return await self.__parent.retrieve(
                    model=self.object,
                    current_user=self.current_user,
                )

            @__parent.router.patch(
                path,
                status_code=status.HTTP_200_OK,
            )
            async def partial_update(
                self, updates: __parent.schemas.PartialUpdate
            ) -> SuccessfullSchema:
                """Partial Updated the Model Fields with ID Primary Key in Path URL"""

                flag = await self.__parent.partial_update(
                    model=self.object,
                    updates=updates,
                    current_user=self.current_user,
                )

                return {
                    "status": flag,
                }

            @__parent.router.delete(
                path,
                status_code=status.HTTP_200_OK,
            )
            async def destroy(self) -> SuccessfullSchema:
                """Delete the Model from Database Table with Primary Key in Path URL"""

                flag = await self.__parent.destroy(
                    model=self.object,
                    current_user=self.current_user,
                )

                return {
                    "status": flag,
                }
