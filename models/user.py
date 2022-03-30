import ormar
import aiofiles
from pydantic import EmailStr
from pathlib import Path
from typing import Optional
from core import (
    Level,
    settings,
    pwd_context,
    MOBILE_PATTERN,
    PrimaryKeyMixin,
)
from db import MainMeta
from schemas import (
    UserInDBSchema,
    UserUpdateSchema,
    ChangePasswordSchema,
)

class User(PrimaryKeyMixin, ormar.Model):
    """User Model Class to Implement Method for Operations of User Entity"""

    mobile: str = ormar.String(unique=True, index=True, max_length=10, pattern=MOBILE_PATTERN)
    password: str = ormar.String(max_length=128)
    level: str = ormar.String(max_length=1, choices=list(Level), default=Level.STAFF.value)
    email: Optional[EmailStr] = ormar.String(max_length=255, nullable=True, default=None)
    avatar: Optional[str] = ormar.String(max_length=255, nullable=True, default=None)
    fullname: Optional[str] = ormar.String(max_length=64, nullable=True, default=None)
    is_active: bool = ormar.Boolean(index=True, default=True)

    @ormar.property_field
    def level_(self) -> Level:
        """Returned the Level Instance of Class Model by Level Value in Database"""

        return Level.get_by_value(value=self.level)

    @classmethod
    async def sign_up(cls, form: UserInDBSchema) -> Optional["User"]:
        """Sign Up method to Register New User with Hashed Password & Check Mobile"""

        if not await cls.objects.filter(mobile=form.mobile).exists():
            if form.avatar is not None:
                form.avatar = await cls.save_avatar(
                    phone_number=form.mobile,
                    avatar=form.base64_decoded(encoded_avatar=form.avatar),
                )

            return await cls.objects.create(**form.dict())

    async def sign_in(self, password: str) -> bool:
        """The Method for Verify Hash Password String Returned Boolean Value"""

        return pwd_context.verify(password, self.password)

    async def edit(self, update_form: UserUpdateSchema) -> bool:
        """Utility Method to Change and Update User Fields by Update Schema Fields"""

        if update_form.mobile is not None:
            if await self.__class__.objects.filter(mobile=update_form.mobile).exists():
                return False

        if update_form.avatar is not None:
            update_form.avatar = await self.save_avatar(
                phone_number=self.mobile,
                avatar=update_form.base64_decoded(encoded_avatar=update_form.avatar)
            )

        await self.update(**update_form.dict(exclude_unset=True))
        return True

    async def change_password(self, passwords: ChangePasswordSchema) -> bool:
        """Utility Method to Change User Password Returned Boolean Value Status"""

        flag = await self.sign_in(password=passwords.old_password)
        if flag:
            await self.update(password=passwords.new_password)

        return flag

    @classmethod
    async def save_avatar(cls, phone_number: str, avatar: bytes) -> str:
        """Saved an Avatar Binary Buffer with Phone Number & Returned the Path"""

        avatar_path = await cls.__get_avatar_path(phone_number=phone_number)
        async with aiofiles.open(avatar_path, "wb") as avatar_file:
            await avatar_file.write(avatar)

        return avatar_path

    @staticmethod
    async def __get_avatar_path(phone_number: str) -> str:
        """Returned the Path of Avatar for this Phone Number & Check Make Directory"""

        users_dir = Path(settings.USER_AVATAR_PATH)
        if not users_dir.exists():
            users_dir.mkdir(parents=True, exist_ok=True)

        return str(users_dir / f"{phone_number}.png")

    class Meta(MainMeta):
        pass
