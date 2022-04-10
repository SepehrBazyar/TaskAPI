from fastapi import status
from httpx import AsyncClient
from typing import Dict, Any
from core import Level
from ...conftest import VERSIONS, FIRST_ADMIN


URL_STR: str = VERSIONS.get("1.0.0") + "user/"


class TestUserRoutes:
    async def test_list_user(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
    ):
        response = await client.get(URL_STR, headers=admin_token_headers)
        content: Dict[str, Any] = response.json()

        assert response.status_code == status.HTTP_200_OK

        assert content["count"] == 1
        assert content["next"] is None
        assert content["previous"] is None

        assert content["results"][0]["mobile"] == FIRST_ADMIN.get("username")
        assert content["results"][0]["level"] == Level.ADMIN.value
        assert content["results"][0]["is_active"] is True

    async def test_create_user(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
    ):
        response = await client.post(
            url=URL_STR,
            headers=admin_token_headers,
            data={
                "mobile": "9123456789",
                "password": "secretpassword",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
