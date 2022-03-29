from fastapi import APIRouter
from .views import generics


router = APIRouter()

for generic in generics:
    router.include_router(
        generic.router, prefix=f"/{generic.name}", tags=[generic.name]
    )
