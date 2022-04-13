from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from uuid import UUID
from typing import Optional, Dict, Literal, Any
from datetime import datetime, timedelta
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/login/")
pwd_context = CryptContext(schemes=["argon2", "pbkdf2_sha256"], deprecated="auto")


class AuthJWT:
    """Security Class to JWT Tokens Operations etc Validations & Generations"""

    def __init__(
        self,
        algorithm: str,
        secret_key: str,
        refresh_expire_day: int,
        access_expire_minute: int,
    ):
        """Saved the Basic Parameters for Generate and Validate JWT Tokens"""

        self.__algorithm = algorithm
        self.__secret_key = secret_key
        self.__refresh_expire_time = timedelta(days=refresh_expire_day)
        self.__access_expire_time = timedelta(minutes=access_expire_minute)

    async def __create_token(
        self,
        subjects: Dict[str, Any],
        *,
        token_type: Literal["access", "refresh"],
    ) -> str:
        """Get a Dictionary Subjects with Token Type Generated a JWT Token"""

        subjects.update({"type": token_type})
        return jwt.encode(subjects, self.__secret_key, algorithm=self.__algorithm)

    async def __decode_token(self, token: str) -> Optional[dict]:
        """Try to Decoded Payload Dict of JWT Token else Returned None Type"""

        try:
            payload = jwt.decode(
                token,
                self.__secret_key,
                algorithms=self.__algorithm,
            )
        except JWTError:
            return None

        return payload

    async def create_access_token(self, user_id: UUID) -> str:
        """Generated and Returned a Access JWT Token to Authentications"""

        data = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + self.__access_expire_time,
        }

        return await self.__create_token(data, token_type="access")

    async def create_refresh_token(self, user_id: UUID) -> str:
        """Generated and Returned a Refresh JWT Token to Authentications"""

        data = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + self.__refresh_expire_time,
        }

        return await self.__create_token(data, token_type="refresh")

    async def get_user_id(self, access_token: str) -> Optional[UUID]:
        """Get the User ID from Access JWT Token if is Validations else None"""

        data = await self.__decode_token(access_token)
        if data is not None and data.get("type") == "access":
            return data.get("user_id")

    async def update_access_token(self, refresh_token: str) -> Optional[str]:
        """Update and Get a New Access JWT Token by Send Valid Refresh Token"""

        data = await self.__decode_token(refresh_token)
        if data is not None and data.get("type") == "refresh":
            return await self.create_access_token(user_id=data.get("user_id"))


jwt_auth = AuthJWT(
    settings.ALGORITHM,
    settings.SECRET_KEY,
    settings.REFRESH_TOKEN_EXPIRE_DAYS,
    settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)
