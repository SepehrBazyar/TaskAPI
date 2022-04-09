from httpx import AsyncClient


class TestUserRoutes:
    async def test_user(self, client: AsyncClient):
        response = await client.get("/v1.0.0/user/")
        assert response.status_code == 401
