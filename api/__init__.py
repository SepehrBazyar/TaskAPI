from v1_0_0 import get_current_user
from .apps import (
    v1_0_0_router,
    v1_0_0,
)


latest, versions = v1_0_0_router, [
    v1_0_0,
]

dependencies = [
    get_current_user,
]
