from models import User
from schemas import UserInDBSchema


class TestUser:
    async def test_create_user(self):
        form = UserInDBSchema(mobile="9123456789", password="1234567890")
        user = await User.sign_up(form=form)
        assert user.id is not None
