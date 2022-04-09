from pytest import MonkeyPatch
from uuid import UUID
from pathlib import Path
from core import settings, Level
from models import User
from schemas import UserInDBSchema


class TestUserModel:
    """Test Cases Class to Methods of User Class Model Entity ORM"""

    __MOBILE, __PASSWORD = "9123456789", "qwerty1234"
    __AVATAR = "iVBORw0KGgoAAAANSUhEUgAAASIAAAEiAQMAAABncE31AAAABlBMVEXMADPMmQAZ5W44AAAFPklEQVR4nJSawa3kNgyGbfgwR5fgFlJAAL9StoQccwgiBznkuCWkhRQQYKeUV8Ic9zBYBpIlm7Qo+YsPgwf6w7OGI1P8SQ7sCiLP8vdHA9gM9dN5b9ya1M8n9WhTy0kt7Scuz/Nem5pfx7J+dKj3sawO9ZDj2e8eVf4MHWqSvLBRvveod/mnHWqUvLBFXl3qme90qEH2u6PIZ5d678vqUmFf2HKx1dTzsuccak0LGyXe6FLvtKwutUhc2P7Zp57R1KVmEXnFZf24o96POyoCEh/7rqnNUuJQ5poi8U1EbRznmsoTu1T6eumL3lHpO3apIT4sPvbzjkpe7VMhAqJd2KCe1tHetUYXrpUfayrtjD61xN951hvHp/a92qfm+NtMeuP4VHo7bqhH8qfeOD71tNHLvabkg7W7cSIVP5cbao/Nc3/jDOMec26oIT1r6m+cYdij3B31JX32N045Ij8aZ2W6NvW/vrSgeHIe6/qlRU2b+o6/tqjHpvz1W4uaN+X731vUsqnfMbSodVN7IrRekLCp/RVanpVN7dXQ+JVG2dS+D419MSWqvEOhsRMfsqn3sbX350SVdzs03rZlDyQ5ToTG+72WcLPulO+wUM6I/OE7LJ8RORYGP2qOkTrjavDj9JSpHKODfzI8RDYV74MfUuZM5bMj+OEpekmdQ8EPiGuhvhXKc1g0q/OxEfSlUEuhHIelVEOd28E92KZC5RwguEdpSkhUPhHEc9hcqJybBPEcFm9tKs+xCYpyV6JKzhTEc1jIt0r+FdyzVDKVn56oymFjolReGLxMYMrUkWMGL/dIv80fKl8N4jhszlRxS6Iqh0V3yZ8qj45U5bB1p86cPFFXhyXjXyq/T4arw2SnjgXs1KfjLvmqdEeiXo675KvSMIn67rhL/lbZc5DaYfNOKc8k6uKw5C759/rPLw5L7pJ/rl/ncFjrHLR2VzNWdlczVlrS1YyVlnQ1Y6UlXc1YaUlXM1Za0tWMlZZ0NWOlJV3NWGlJVzNWWtLVjJWWdDVjrSU9zThUdk8zDpXd04xDZfc041DZPc04VHZPMw6V3dOMQ2X3NGNt9zRjbfc0Y233NGNtt5oxHC+rtVvNeFLWbjXjhTrsVjOelLVbzWgppSWNZjypi5Y0mtFSSksazagoqyWNZrSU0pJGMyrKakmjGS2ltKTRjIqyWtJoRkNpLWk0o6KsljSa0VBaSxrNqCirJY1mNJTWkkYzKspqSaMZDaXsVjMqympJoxk1ZbWk1oyKumhJrRk1ZbWk1oyaslryQ31qStvp/2LrQt+R+Yv5nv2ObE+w/cX2Ktv37B1i7yN7t1mcYDGHxS8WC1lcRTGaxXt2drBziJ1pXk21trOzlp3bLAdg+QTLTView3Imln+xXI7lhSjHZPkqy31ZHs1ycpbfM63AdAfTMEwPMW3FdBrTfPnR6c3TW6e23GvRvMBku9O1TCMzvc20O6sDsJoCrE+wWgerm7AaDKvnsNoQqzOxmhWsf7FaGqvLsRofqxey2iOrY7KaKKyvslotq/uyGjKrR7PaNquTs5o7rN+zXgDrK7AeBet3sN4J68Owng7sD7FeE+tbsR4Y66ex3hzr87Ge4VBpxtbFepmsL4p6rKxfy3q/rI/MetKsv8165azvznr4bB6AzRawOQU288DmJ9gsBpvrQDMibN6Eza6wOZjmTE09xSP+FA+b9fm/c0NsBonNM7HZKDZnxWa22PwXmyVjc2loxo3Ny7HZOzbHx2YC2Xwhm1Vkc49shpLNY7LZTjYn2p45Rdd/AQAA//9/35AUGS3FfQAAAABJRU5ErkJggg=="  # noqa: E501

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

    async def test_create_admin_user(self):
        form = UserInDBSchema(
            level=Level.ADMIN,
            mobile=self.__MOBILE,
            password=self.__PASSWORD,
        )
        user = await User.sign_up(form=form)

        assert user.level_ is Level.ADMIN
        assert isinstance(user.level, str)

    async def test_create_avatar_user(self, monkeypatch: MonkeyPatch):
        get_path = lambda mobile: str(Path(settings.USER_AVATAR_PATH) / f"{mobile}.png")

        async def mock_save_avatar(phone_number: str, avatar: bytes) -> str:
            """Mocked Saved Binary Buffer Avatar Method with Returned the Path"""

            return get_path(mobile=phone_number)

        monkeypatch.setattr(target=User, name="save_avatar", value=mock_save_avatar)

        form = UserInDBSchema(
            avatar=self.__AVATAR,
            mobile=self.__MOBILE,
            password=self.__PASSWORD,
        )
        user = await User.sign_up(form=form)

        assert user.avatar == get_path(mobile=self.__MOBILE)

    async def test_login_password_user(self):
        form = UserInDBSchema(mobile=self.__MOBILE, password=self.__PASSWORD)
        user = await User.sign_up(form=form)

        assert await user.sign_in(password=self.__PASSWORD) is True
        assert await user.sign_in(password="wrongpassword") is False
