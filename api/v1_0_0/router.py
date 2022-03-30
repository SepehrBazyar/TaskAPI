from fastapi import APIRouter
from .views import cbvs


router = APIRouter()


for cbv in cbvs:
    router.include_router(cbv.router, prefix=f"/{cbv.name}", tags=[cbv.name])
