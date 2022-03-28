from fastapi import Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter
from core import jwt_auth
from models import User, UserSerializer
from schemas import (
    AccessTokenSchema,
    RefreshTokenSchema,
)
from api.base import BaseAPIView, GenericAPIView


router = InferringRouter()


class UserGenericAPIView(GenericAPIView):
    """Generic Class Based Views for User Model Override Some of Methods"""

    async def perform_create(self, model_form: UserSerializer.Shcema.Create) -> User:
        """Perform Create Method Called Before Create & Use Sign Up User Method"""

        new_user = await User.sign_up(form=model_form)
        if new_user is None:
            raise ValueError("Phone Number Already Existed.")

        return new_user


generic = UserGenericAPIView(router, serializer=UserSerializer)


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


generic.list_create()
