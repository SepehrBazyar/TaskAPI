import re as regex
from pydantic import Field, EmailStr, validator, root_validator
from magic import from_buffer
from base64 import b64decode
from typing import Optional, List, Dict
from core import (
    Level,
    settings,
    BaseModel,
    Pagination,
    pwd_context,
    MOBILE_PATTERN,
    PrimaryKeySchema,
    ValidUpdateMixinSchema,
)


def get_password_hash(password: str) -> str:
    """Reusable Validator Method Utility for Generate Hash Password String"""

    return pwd_context.hash(secret=password)


class UserBriefSchema(PrimaryKeySchema):
    """Schema of the Brief Detials User to Showing in Users List"""

    mobile: str
    level: Level
    is_active: bool


class OptionalFieldSchema(BaseModel):
    """Schema to Shared Fields of User Model is Optional Can be None"""

    email: Optional[EmailStr] = Field(default=None)
    fullname: Optional[str] = Field(default=None, max_length=64)


class AvatarMixinSchema(BaseModel):
    """Schema to Validate Avatar Field of User Check be Valid Encoded PNG"""

    avatar: Optional[str] = Field(default=None)

    @validator("avatar")
    def check_valid_png(cls, value: Optional[str]) -> Optional[str]:
        """Check the Avatar Base 64 Encoded is Valid PNG Mime Type Raised Error"""

        if value is not None:
            decoded_avatar = cls.base64_decoded(encoded_avatar=value)
            if decoded_avatar is not None:
                if from_buffer(buffer=decoded_avatar, mime=True) == "image/png":
                    return value

            raise ValueError("Avatar Should be PNG.")

    @staticmethod
    def base64_decoded(encoded_avatar: str) -> Optional[bytes]:
        """Decoded the Base 64 Encoded Avatar if is Valid String Else None"""

        pattern = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        if regex.match(pattern=pattern, string=encoded_avatar):
            return b64decode(encoded_avatar)


class UserInDBSchema(OptionalFieldSchema, AvatarMixinSchema):
    """Schema to Create New User with Password Field Hash & Save It"""

    mobile: str = Field(regex=MOBILE_PATTERN)
    password: str = Field(min_length=8, max_length=128)
    level: Level = Field(default=Level.STAFF)
    is_active: bool = Field(default=True)

    # validators
    _password_hashing = validator("password", allow_reuse=True)(get_password_hash)


class UserOutDBSchema(UserBriefSchema, OptionalFieldSchema):
    """Schema to Retrieve User Details Information not Contain Password"""

    avatar: Optional[str] = Field(default=None)

    @validator("avatar")
    def avatar_path_url(cls, value: Optional[str]) -> Optional[str]:
        """Validator to Added Base URL Prefix to Avatar Path Saved if not None"""

        if value is not None:
            return settings.BASE_URL + value


class UserSelfUpdateSchema(
    OptionalFieldSchema, AvatarMixinSchema, ValidUpdateMixinSchema
):
    """Schema for Update Self User Fields All is Optional Items Remove Unsets"""

    mobile: Optional[str] = Field(default=None, regex=MOBILE_PATTERN)
    is_active: Optional[bool] = Field(default=None)


class UserUpdateSchema(UserSelfUpdateSchema):
    """Schema for Update User Fields All is Optional Items Remove Unsets"""

    level: Optional[Level] = Field(default=None)


class UserListSchema(Pagination):
    """Schema of Users List with Pagination Items Count & Next & Previous"""

    results: List[UserBriefSchema] = Field(default=[])


class UserFilterSchema(BaseModel):
    """Schema to Filter User List by Query Parameters Value"""

    level: Optional[Level] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class AccessTokenSchema(BaseModel):
    """Schema of the Update New Access JWT Token with Token Bearer Type"""

    token_type: str = Field(default="bearer")
    access_token: str


class RefreshTokenSchema(AccessTokenSchema):
    """Schema of the Login JWT Token Inheritance Update with Refresh Token"""

    refresh_token: str


class ChangePasswordSchema(BaseModel):
    """Schema of Get Old & New Password of User to Update & Change Password"""

    old_password: str = Field(max_length=128)
    new_password: str = Field(max_length=128)
    confirm_password: str = Field(max_length=128)

    # validators
    _password_hashing = validator("new_password", allow_reuse=True)(get_password_hash)

    @root_validator(pre=True)
    def check_passwords_match(cls, values: Dict[str, str]) -> Dict[str, str]:
        """Validator to Check Matchs New Password & Confirm Password Field"""

        new, confirm = values.get("new_password"), values.get("confirm_password")
        if not new == confirm:
            raise ValueError("Passwords Do not Match.")

        return values
