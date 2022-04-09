from uuid import UUID
from core import Level
from models import User
from schemas import UserInDBSchema


class TestUserModel:
    """Test Cases Class to Methods of User Class Model Entity ORM"""

    __MOBILE, __PASSWORD = "9123456789", "qwerty1234"

    async def test_create_simple_user(self):
        form = UserInDBSchema(mobile=self.__MOBILE, password=self.__PASSWORD)
        user = await User.sign_up(form=form)

        assert user is not None
        assert isinstance(user.id, UUID)

    async def test_create_duplicate_user(self):
        form = UserInDBSchema(mobile=self.__MOBILE, password=self.__PASSWORD)

        user1 = await User.sign_up(form=form)
        assert user1 is not None

        user2 = await User.sign_up(form=form)
        assert user2 is None
