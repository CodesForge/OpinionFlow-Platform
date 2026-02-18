from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from functools import lru_cache

@lru_cache
def get_authX_settings() -> "AuthX_Settings":
    return AuthX_Settings()

class AuthX_Settings(BaseSettings):
    algorithm: str = Field(default="HS256", alias="AUTH_JWT_ALGORITHM")
    secret_key: str = Field(alias="AUTH_JWT_SECRET_KEY")
    expires: int = Field(default=3600, alias="AUTH_JWT_EXPIRES")
    
    model_config = SettingsConfigDict(
        env_file="src/env/authx_settings.env", env_file_encoding="utf-8",
    )