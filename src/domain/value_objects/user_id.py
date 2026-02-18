"""
UserID value object.

Represents a unique identifier for users using UUID.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Self


@dataclass(frozen=True, slots=True)
class UserID:
    """
    User identifier value object.
    
    Uses UUID4 for unique identification.
    Immutable (frozen) for safety.
    
    Attributes:
        value: The UUID value of the user ID.
    """
    
    value: UUID = field(default_factory=uuid4)

    @classmethod
    def next(cls) -> Self:
        """
        Creates a new unique UserID instance.
        
        Generates a new UUID4 for each call.
        
        Returns:
            Self: New UserID instance with unique UUID.
        """
        return cls()
