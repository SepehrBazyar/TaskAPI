from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings Class to Read Environment Variable Parameters"""

    # Security
    BASE_URL: str
    ALGORITHM: str
    SECRET_KEY: str
    ALLOWED_HOSTS: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool

    # Databases
    POSTGRESQL_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
