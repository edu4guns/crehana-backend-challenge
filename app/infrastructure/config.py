from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Backend Challenge"
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@db:5432/crehana_db",
        alias="DATABASE_URL",
    )
    jwt_secret_key: str = Field(
        default="changeme", alias="JWT_SECRET_KEY"
    )  # en prod se debe reemplazar
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

