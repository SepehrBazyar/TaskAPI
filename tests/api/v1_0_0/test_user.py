from httpx import AsyncClient
from typing import Dict
from ...conftest import VERSIONS


URL_STR = VERSIONS.get("1.0.0") + "user/"


class TestUserRoutes:
    async def test_get_user(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
    ):
        response = await client.get(URL_STR, headers=admin_token_headers)
