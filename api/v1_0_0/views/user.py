from fastapi import Request, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from core import (
    Level,
    jwt_auth,
    ItemsPerPage,
    PrimaryKeySchema,
    SuccessfullSchema,
)
from models import User
from schemas import (
    UserListSchema,
    UserInDBSchema,
    UserOutDBSchema,
    UserUpdateSchema,
    UserFilterSchema,
    AccessTokenSchema,
    RefreshTokenSchema,
    UserSelfUpdateSchema,
    ChangePasswordSchema,
)
from decorators import check_user_level
from ..deps import BaseAPIView, get_user


router = InferringRouter()


class UserAPIView(BaseAPIView):
    """Basic Class Based View for CRUD Operations for User Entity Model"""

    model, router = User, router
    name = model.get_name(lower=True)


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
) -> RefreshTokenSchema:
    """Authorize View Get Username & Password to Login User Returned JWT Token"""

    user = await User.objects.get_or_none(mobile=form.username, is_active=True)
    if user is not None and await user.sign_in(password=form.password):
        return {
            "access_token": await jwt_auth.create_access_token(user_id=user.id),
            "refresh_token": await jwt_auth.create_refresh_token(user_id=user.id),
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Phone Number or Password Incorrect.",
    )


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
)
async def refresh(
    refresh: str = Body(..., embed=True),
) -> AccessTokenSchema:
    """View to Obtain New Updated JWT Access Token by Sent the Refresh Token in Body"""

    access_token = await jwt_auth.update_access_token(refresh_token=refresh)
    if access_token is not None:
        return {
            "access_token": access_token,
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh Token is not Valid."
    )


@cbv(router)
class UserListCreateAPIView(UserAPIView):
    """Class Based View for List & Create Operations for User Model"""

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
        params: UserFilterSchema = Depends(),
    ) -> UserListSchema:
        """Returned the List of User with Brief Details in Pagination Mode"""

        count, next, previous, queryset = await self.get_list(
            url=request.url, pagination=pagination, **params.dict(exclude_none=True)
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
    async def create(self, user_form: UserInDBSchema) -> PrimaryKeySchema:
        """Registering New User Model with Sign Up & Returned Primary Key UUID"""

        new_user = await self.model.sign_up(form=user_form)
        if new_user is not None:
            return new_user

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone Number Already Existed.",
        )


@cbv(router)
class UserSelfAPIView(UserAPIView):
    """Class Based View for See and Edit Profile Operations for Self User Model"""

    __PATH = "/profile/"

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    async def show_profile(self) -> UserOutDBSchema:
        """Showing the Profile Detail Item Fields of this Current User"""

        return self.current_user


    @router.patch(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    async def edit_profile(self, fields: UserSelfUpdateSchema) -> SuccessfullSchema:
        """Edit the Profile Detail Item Fields of this Current User"""

        flag = await self.current_user.edit(update_form=fields)
        if flag:
            return SuccessfullSchema()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Update Data Failed."
        )


    @router.post(
        "/change-password/",
        status_code=status.HTTP_200_OK,
    )
    async def change_password(
        self,
        passwords: ChangePasswordSchema,
    ) -> SuccessfullSchema:
        """Change & Update the Password of this Current User with Check Correctly"""

        flag = await self.current_user.change_password(passwords=passwords)
        if flag:
            return SuccessfullSchema()
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Password."
        )


@cbv(router)
class UserRetrieveUpdateDestroyAPIView(UserAPIView):
    """Class Based View for Retrieve Update Destroy Operations for User Model"""

    __PATH = "/{user_id}/"

    user: User = Depends(get_user)

    @router.get(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def retrieve(self) -> UserOutDBSchema:
        """Retrieve the User Information Details by Get Primary Key ID in Path"""

        return self.user


    @router.patch(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def partial_update(self, fields: UserUpdateSchema) -> SuccessfullSchema:
        """Updated the User Information Detail with ID Primary Key in Path URL"""

        flag = await self.user.edit(update_form=fields)
        if flag:
            return SuccessfullSchema()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Update Data Failed."
        )


    @router.delete(
        __PATH,
        status_code=status.HTTP_200_OK,
    )
    @check_user_level(Level.ADMIN)
    async def destroy(self) -> SuccessfullSchema:
        """Delete the User Model from Database Table with Input ID in Path URL"""

        await self.user.delete()
        return SuccessfullSchema()
