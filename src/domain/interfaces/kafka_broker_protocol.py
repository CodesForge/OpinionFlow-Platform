"""
Kafka broker protocol.

Interface for message broker operations (publish/subscribe).
"""

from typing import Protocol, Dict, Any


class KafkaBrokerProtocol(Protocol):
    """
    Protocol for Kafka message broker implementation.
    
    Defines the interface for publishing events to Kafka topics.
    Uses structural subtyping (Protocol) for dependency inversion.
    
    Responsibilities:
    - Publish events to Kafka topics
    - Serialize events to JSON/Avro format
    - Handle connection errors and retries
    
    Example implementations:
    - KafkaBroker (production, with full Kafka client)
    - InMemoryBroker (testing, mock implementation)
    
    Example usage:
        broker = KafkaBroker(bootstrap_servers=["localhost:9092"])
        await broker.publish("user-events", {"event": "user_registered", "user_id": 123})
    """

    async def publish(self, topic: str, event: Dict[str, Any]) -> None:
        """
        Publishes an event to a Kafka topic.
        
        Serializes the event to JSON/Avro format and sends it to the specified topic.
        The message is persisted in Kafka and becomes available to all consumers.
        
        Args:
            topic: Kafka topic name to publish to (e.g., "user-events", "post-created").
            event: Event data as dictionary. Must be JSON-serializable.
                   Example: {"event": "user_registered", "user_id": 123, "timestamp": "2026-02-18T14:00:00Z"}
        
        Raises:
            KafkaError: If connection to Kafka broker fails.
            SerializationError: If event cannot be serialized.
            Exception: On other unexpected errors.
        
        Example:
            await broker.publish(
                topic="user-events",
                event={
                    "event": "user_registered",
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "alex",
                    "timestamp": "2026-02-18T14:00:00Z"
                }
            )
        """
        ...
