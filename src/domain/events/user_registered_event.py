"""
User Registered domain event.

Raised when a new user registers in the system.
"""

from dataclasses import dataclass, field

from src.domain.value_objects.user_id import UserID
from src.domain.events.domain_event import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class UserRegisteredEvent(DomainEvent):
    """
    Event raised when a new user registers.
    
    Used to notify other parts of the system about user registration.
    Can trigger actions like sending welcome emails, analytics, etc.
    
    Attributes:
        user_id: ID of the newly registered user.
    """
    
    user_id: UserID

    def payload(self) -> dict:
        """
        Returns the event payload.
        
        Returns:
            dict: Event data containing user_id.
        """
        return {"user_id": str(self.user_id)}
