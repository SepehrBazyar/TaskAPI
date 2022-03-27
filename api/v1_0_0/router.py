from fastapi import APIRouter
from .views import (
    user_router,
)


router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
