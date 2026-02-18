"""
Username value object.

Represents a validated username with length constraints.
"""

from dataclasses import dataclass
from typing import Self

from src.domain.exceptions.domain import ValidationError


@dataclass(frozen=True, slots=True)
class Username:
    """
    Username value object with validation.
    
    Constraints:
    - Minimum length: 3 characters
    - Maximum length: 15 characters
    - Must be a string
    
    Attributes:
        value: The username string value.
    """
    
    _MIN_LEN = 3  # Minimum username length
    _MAX_LEN = 15  # Maximum username length
    value: str

    def __post_init__(self) -> None:
        """
        Validates username after initialization.
        
        Raises:
            ValidationError: If username is not a string.
            ValidationError: If username length is invalid.
        """
        if not isinstance(self.value, str):
            raise ValidationError(
                "Username must be a string"
            )
        if len(self.value) < self._MIN_LEN:
            raise ValidationError(
                f"Username cannot be less than {self._MIN_LEN} characters"
            )
        if len(self.value) > self._MAX_LEN:
            raise ValidationError(
                f"Username cannot be more than {self._MAX_LEN} characters"
            )

    @classmethod
    def create(cls, raw_username: str) -> Self:
        """
        Creates a validated Username instance.
        
        Args:
            raw_username: Raw username string to validate.
            
        Returns:
            Self: Validated Username instance.
        """
        return cls(raw_username.strip())
