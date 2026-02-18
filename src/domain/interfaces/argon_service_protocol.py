"""
Argon service protocol.

Interface for password hashing service implementation.
"""

from typing import Protocol


class ArgonServiceProtocol(Protocol):
    """
    Protocol for Argon2 password hashing service.
    
    Defines the interface that all password hashing implementations
    must follow. Uses structural subtyping (Protocol).
    
    Example implementation:
        class ArgonService(ArgonServiceProtocol):
            async def hash(self, password: str) -> str: ...
            async def verify(self, hash: str, password: str) -> bool: ...
    """

    async def hash(self, password: str) -> str:
        """
        Hashes a plain text password using Argon2.
        
        Args:
            password: Plain text password to hash.
            
        Returns:
            str: Argon2 hashed password.
        """
        ...

    async def verify(self, hash: str, password: str) -> bool:
        """
        Verifies if plain password matches the hash.
        
        Args:
            hash: Argon2 hashed password.
            password: Plain text password to verify.
            
        Returns:
            bool: True if password matches hash, False otherwise.
        """
        ...
