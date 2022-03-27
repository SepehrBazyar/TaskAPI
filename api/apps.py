from core import VersionFastAPI
from .v1_0_0 import router as v1_0_0_router


v1_0_0 = VersionFastAPI(1, 0, 0)()
v1_0_0.include_router(v1_0_0_router)
