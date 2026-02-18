"""
Domain Event base class.

Abstract base class for all domain events in the system.
"""

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from typing import Dict, Any
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class DomainEvent(ABC):
    """
    Base class for all domain events.
    
    Domain events represent something that happened in the domain.
    They are immutable and contain all relevant data about the event.
    
    Attributes:
        event_id: Unique event identifier (UUID4).
        occurred_at: Timestamp when the event occurred (UTC).
    """
    
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @abstractmethod
    def payload(self) -> Dict[str, Any]:
        """
        Returns the event payload as a dictionary.
        
        Must be implemented by all concrete event classes.
        
        Returns:
            Dict[str, Any]: Event data as dictionary.
        """
        ...

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the event to a dictionary representation.
        
        Includes metadata (event_id, event_type, occurred_at)
        and event-specific payload.
        
        Returns:
            Dict[str, Any]: Complete event data as dictionary.
        """
        return {
            "event_id": str(self.event_id),
            "event_type": self.__class__.__name__,
            "occurred_at": self.occurred_at.isoformat(),
            "data": self.payload(),
        }
