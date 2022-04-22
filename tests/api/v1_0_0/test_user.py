from fastapi import status
from httpx import AsyncClient
from typing import Dict, Any
from core import Level
from ...conftest import VERSIONS, FIRST_ADMIN


URL_STR: str = VERSIONS.get("1.0.0") + "user/"


class TestUserRoutes:
    """Test Cases Class for Test APIs of User Entity Model Routes"""

    async def test_login_failed_username_user(
        self,
        client: AsyncClient,
    ):
        response = await client.post(
            url=URL_STR + "login/",
            data={
                "username": "wrongusername",
                "password": FIRST_ADMIN.get("password"),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    async def test_login_failed_password_user(
        self,
        client: AsyncClient,
    ):
        response = await client.post(
            url=URL_STR + "login/",
            data={
                "username": FIRST_ADMIN.get("username"),
                "password": "wrongpassword",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_login_successfull_user(
        self,
        client: AsyncClient,
    ):
        response = await client.post(url=URL_STR + "login/", data=FIRST_ADMIN)

        assert response.status_code == status.HTTP_200_OK

        content: Dict[str, Any] = response.json()

        assert "token_type" in content
        assert "access_token" in content
        assert "refresh_token" in content

    async def test_refresh_failed_user(
        self,
        client: AsyncClient,
    ):
        response = await client.post(
            url=URL_STR + "refresh/",
            json={
                "refresh": "fakerefreshtoken",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_refresh_successfull_user(
        self,
        client: AsyncClient,
    ):
        response = await client.post(url=URL_STR + "login/", data=FIRST_ADMIN)
        tokens: Dict[str, Any] = response.json()

        response = await client.post(
            url=URL_STR + "refresh/",
            json={
                "refresh": tokens.get("refresh_token"),
            },
        )

        assert response.status_code == status.HTTP_200_OK

        content: Dict[str, Any] = response.json()

        assert "token_type" in content
        assert "access_token" in content

    async def test_list_user(
        self,
        client: AsyncClient,
        admin_token_headers: Dict[str, str],
    ):
        response = await client.get(URL_STR, headers=admin_token_headers)

        assert response.status_code == status.HTTP_200_OK

        content: Dict[str, Any] = response.json()

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
            json={
                "mobile": "9123456789",
                "password": "secretpassword",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
