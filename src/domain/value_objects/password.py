"""
Password value object.

Represents a hashed password with validation and verification capabilities.
"""

from dataclasses import dataclass
from typing import Self

from src.domain.interfaces.argon_service_protocol import ArgonServiceProtocol
from src.domain.exceptions.domain import ValidationError


@dataclass(frozen=True, slots=True)
class Password:
    """
    Password value object with hashing support.
    
    Constraints:
    - Minimum length: 8 characters
    - Maximum length: 25 characters
    - Stored as Argon2 hash
    
    Attributes:
        value: The hashed password string.
    """
    
    _MIN_LEN = 8  # Minimum password length
    _MAX_LEN = 25  # Maximum password length
    value: str

    @classmethod
    async def create(cls, plain_password: str, hasher: ArgonServiceProtocol) -> Self:
        """
        Creates a hashed Password instance from plain text password.
        
        Args:
            plain_password: Raw password string to hash.
            hasher: Argon2 hashing service implementation.
            
        Returns:
            Self: Password instance with hashed value.
            
        Raises:
            ValidationError: If password length is invalid.
        """
        if len(plain_password) < cls._MIN_LEN:
            raise ValidationError(
                f"The password cannot be less than {cls._MIN_LEN} characters"
            )
        if len(plain_password) > cls._MAX_LEN:
            raise ValidationError(
                f"The password cannot be more than {cls._MAX_LEN} characters"
            )
        hash = await hasher.hash(plain_password)
        return cls(value=hash)

    async def verify(self, plain_password: str, hasher: ArgonServiceProtocol) -> bool:
        """
        Verifies if plain password matches the stored hash.
        
        Args:
            plain_password: Raw password string to verify.
            hasher: Argon2 hashing service implementation.
            
        Returns:
            bool: True if password matches, False otherwise.
        """
        return await hasher.verify(self.value, plain_password)
