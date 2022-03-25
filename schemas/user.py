import re as regex
from pydantic import Field, EmailStr, validator, root_validator
from magic import from_buffer
from base64 import b64decode
from typing import Optional, List, Dict
from core import (
    Level,
    BaseModel,
    Pagination,
    UUIDSchema,
    MOBILE_PATTERN,
)


class UserBriefSchema(UUIDSchema):
    """Schema of the Brief Detials User to Showing in Users List"""

    mobile: str
    level: Level


class UserAvatarValidatorSchema(BaseModel):
    """Schema to Validate Avatar Field of User Check be Valid Encoded PNG"""

    @validator('avatar')
    def check_valid_png(cls, value: Optional[str]) -> Optional[str]:
        """Check the Avatar Base 64 Encoded is Valid PNG Mime Type Raised Error"""

        if value is not None:
            decoded_avatar = cls.base64_decoded(encoded_avatar=value)
            if decoded_avatar is not None:
                if not from_buffer(buffer=decoded_avatar, mime=True) == "image/png":
                    return value

            raise ValueError("Avatar Should be PNG.")

    @staticmethod
    def base64_decoded(encoded_avatar: str) -> Optional[bytes]:
        """Decoded the Base 64 Encoded Avatar if is Valid String Else None"""

        pattern = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        if regex.match(pattern=pattern, string=encoded_avatar):
            return b64decode(encoded_avatar)


class UserInDBSchema(UserAvatarValidatorSchema):
    """Schema to Create New User with Password Field Hash & Save It"""

    mobile: str = Field(regex=MOBILE_PATTERN)
    password: str = Field(max_length=128)
    level: Level = Field(default=Level.EMPLOYEE)
    email: Optional[EmailStr] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    fullname: Optional[str] = Field(default=None, max_length=64)
    is_active: bool = Field(default=True)


class UserOutDBSchema(UserBriefSchema):
    """Schema to Retrieve User Details Information not Contain Password"""

    email: Optional[EmailStr] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    fullname: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)


class UserUpdateSchema(UserAvatarValidatorSchema):
    """Schema for Update User Fields All is Optional Items Remove Unsets"""

    mobile: Optional[str] = Field(default=None, regex=MOBILE_PATTERN)
    level: Optional[Level] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    fullname: Optional[str] = Field(default=None, max_length=64)
    is_active: Optional[bool] = Field(default=None)


class UserListSchema(Pagination):
    """Schema of Users List with Pagination Items Count & Next & Previous"""

    results: List[UserBriefSchema] = Field(default=[])


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

    @root_validator
    def check_passwords_match(cls, values: Dict[str, str]) -> Dict[str, str]:
        """Validator to Check Matchs New Password & Confirm Password Field"""

        new, confirm = values.get("new_password"), values.get("confirm_password")
        if not new == confirm:
            raise ValueError("Passwords Do not Match.")

        return values
