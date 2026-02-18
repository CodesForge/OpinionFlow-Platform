"""
User aggregate root.

Represents a user entity in the domain with all business logic.
"""

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import List, Self

from src.domain.value_objects.user_id import UserID
from src.domain.value_objects.username import Username
from src.domain.value_objects.password import Password
from src.domain.events.domain_event import DomainEvent
from src.domain.interfaces.argon_service_protocol import ArgonServiceProtocol
from src.domain.events.user_registered_event import UserRegisteredEvent


@dataclass(frozen=True, slots=True)
class User:
    """
    User aggregate root entity.
    
    Contains all user-related data and business logic.
    Immutable after creation (frozen).
    Implements Domain Events pattern.
    
    Attributes:
        user_id: Unique user identifier.
        username: Validated username value object.
        password: Hashed password value object.
        created_at: User registration timestamp.
        _events: List of domain events (internal).
    """
    
    user_id: UserID
    username: Username
    password: Password
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _events: List["DomainEvent"] = field(default_factory=list, repr=False, init=False)

    @classmethod
    async def create(cls, raw_username: str, plain_password: str, hasher: ArgonServiceProtocol) -> Self:
        """
        Factory method to create a new User instance.
        
        Validates username and password, hashes password,
        and raises UserRegisteredEvent.
        
        Args:
            raw_username: Raw username string to validate.
            plain_password: Raw password string to hash.
            hasher: Argon2 hashing service implementation.
            
        Returns:
            Self: New User instance with domain events.
        """
        user_id = UserID.next()
        username = Username.create(raw_username)
        password = await Password.create(plain_password, hasher)

        user = cls(
            user_id=user_id,
            username=username,
            password=password,
        )
        object.__setattr__(
            user, 
            "_events", 
            [UserRegisteredEvent(user_id=user_id.value)]
        )
        return user

    def pull_events(self) -> List["DomainEvent"]:
        """
        Retrieves and clears all pending domain events.
        
        Called by infrastructure layer after saving user.
        
        Returns:
            List[DomainEvent]: List of events to be processed.
        """
        event = self._events.copy()
        object.__setattr__(self, "_events", [])
        return event
