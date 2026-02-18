from faststream.kafka import KafkaBroker
from faststream import FastStream
from typing import Optional, Dict, Any

from src.domain.interfaces.kafka_broker_protocol import KafkaBrokerProtocol
from src.config.kafka_broker_settings import KafkaBrokerSettings
from src.common.logger import logger

class KafkaMessageBroker(KafkaBrokerProtocol):
    def __init__(self, settings: KafkaBrokerSettings):
        self._settings = settings
        self._broker: Optional[KafkaBroker] = None
        self._router: Optional[FastStream] = None
    
    @property
    def broker(self) -> KafkaBroker:
        if self._broker is None:
            try:
                self._broker = KafkaBroker(
                    self._settings.broker_url,
                )
                logger.info(
                    "Kafka-broker successfully initialized"
                )
            except Exception as e:
                logger.exception(
                    f"Kafka-broker initialization error: {e}"
                )
                raise
        return self._broker

    @property
    def router(self) -> FastStream:
        if self._router is None:
            try:
                self._router = FastStream(
                    self.broker,
                )
                logger.info(
                    "Kafka-router successfully initialized"
                )
            except Exception as e:
                logger.exception(
                    f"Kafka-router initialization error: {e}"
                )
                raise
        return self._router
    
    async def publish(self, event: Dict[str, Any], topic: str) -> None:
        try:
            await self.broker.publish(
                message=event, topic=topic
            )
            logger.info(
                f"Message '{event}' was successfully sent to '{topic}'"
            )
        except Exception as e:
            logger.exception(
                f"Errors sending message '{event}' to '{topic}': {e}"
            )
            raise
    