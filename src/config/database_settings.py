from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

@lru_cache(maxsize=1)
def get_database_settings() -> "DatabaseSettings":
    return DatabaseSettings() 

class DatabaseSettings(BaseSettings):
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    db: str = Field(alias="POSTGRES_DB")
    host: str = Field(alias="DB_HOST")
    port: int = Field(alias="DB_PORT")
    
    @property
    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db}"
        )
    
    model_config = SettingsConfigDict(
        env_file="src/env/database_settings.env",
        env_file_encoding="utf-8",
    )