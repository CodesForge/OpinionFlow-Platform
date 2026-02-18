from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

@lru_cache
def get_argon_settings() -> "ArgonSettings":
    return ArgonSettings()

class ArgonSettings(BaseSettings):
    time_cost: int = Field(default=3, alias="TIME_COST")
    parallelism: int = Field(default=4, alias="PARALLELISM")
    hash_len: int = Field(default=32, alias="HASH_LEN")
    salt_len: int = Field(default=16, alias="SALT_LEN")
    memory_cost: int = Field(default=65536, alias="MEMORY_COST")
    
    model_config = SettingsConfigDict(
        env_file="src/env/argon_service_settings.env",
        env_file_encoding="utf-8",
    )