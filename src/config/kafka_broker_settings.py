from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

@lru_cache(maxsize=1)
def get_kafka_broker_settings() -> "KafkaBrokerSettings":
    return KafkaBrokerSettings()

class KafkaBrokerSettings(BaseSettings):
    broker_url: str = Field(
        default="kafka:29092",
        alias="BROKER_URL",
    )
    
    model_config = SettingsConfigDict(
        env_file="src/env/kafka_broker_settings.env",
        env_file_encoding="utf-8",
    )