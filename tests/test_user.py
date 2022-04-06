from pytest import mark
from schemas import UserInDBSchema
from models import User


@mark.asyncio
class TestUser:
    async def test_create_user(self):
        form = UserInDBSchema(mobile="9123456789", password="1234567890")
        user = await User.sign_up(form=form)
        assert user.id is not None
