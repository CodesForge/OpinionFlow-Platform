"""
Argon2 password hashing service.

Production-ready password hashing implementation using Argon2.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
import asyncio

from src.common.logger import logger
from src.domain.interfaces.argon_service_protocol import ArgonServiceProtocol
from src.config.argon_service_settings import ArgonSettings


class ArgonService(ArgonServiceProtocol):
    """
    Argon2 password hashing service.
    
    Implements secure password hashing and verification
    using the Argon2id algorithm (winner of Password Hashing Competition).
    
    Features:
    - Async operations (non-blocking)
    - Lazy initialization
    - OWASP recommended parameters
    
    Example:
        service = ArgonService(settings)
        hashed = await service.hash("mypassword")
        is_valid = await service.verify(hashed, "mypassword")
    """

    def __init__(self, settings: ArgonSettings):
        """
        Initialize Argon2 hashing service.
        
        Args:
            settings: Argon2 configuration parameters.
        """
        self._settings = settings
        self._ph: PasswordHasher | None = None

    @property
    def ph(self) -> PasswordHasher:
        """
        Returns PasswordHasher instance with lazy initialization.
        
        Creates PasswordHasher on first access with configured parameters.
        Lazy init saves resources — created only when needed.
        
        Returns:
            PasswordHasher: Configured Argon2 hasher.
            
        Raises:
            Exception: If hasher initialization fails.
        """
        if self._ph is None:
            try:
                # Create PasswordHasher with config settings
                # Use OWASP recommendations if settings not provided
                self._ph = PasswordHasher(
                    time_cost=self._settings.time_cost,
                    memory_cost=self._settings.memory_cost,
                    parallelism=self._settings.parallelism,
                    hash_len=self._settings.hash_len,
                    salt_len=self._settings.salt_len,
                )
                logger.info("Argon2 password hasher initialized successfully")
            except Exception as e:
                logger.error(f"Argon2 password hasher initialization error: {e}")
                raise
        return self._ph

    async def hash(self, password: str) -> str:
        """
        Hashes a plain text password using Argon2id.
        
        Args:
            password: Plain text password to hash.
            
        Returns:
            str: Argon2 hashed password.
            
        Raises:
            ValueError: If password is empty.
            Exception: If hashing fails.
        """
        # Check password is not empty
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            # Run blocking operation in separate thread
            # asyncio.to_thread does not block event loop
            # Other requests can be processed while hashing
            return await asyncio.to_thread(self.ph.hash, password)
        except Exception as e:
            logger.error(f"Password hashing error: {e}")
            raise

    async def verify(self, hash: str, password: str) -> bool:
        """
        Verifies if plain password matches the Argon2 hash.
        
        Args:
            hash: Argon2 hashed password.
            password: Plain text password to verify.
            
        Returns:
            bool: True if password matches hash, False otherwise.
            
        Raises:
            InvalidHash: If hash format is invalid.
        """
        # Check hash and password are not empty
        if not hash or not password:
            return False
        
        try:
            # Run blocking operation in separate thread
            # verify() can take 1-2 seconds
            # to_thread allows processing other requests in parallel
            return await asyncio.to_thread(self.ph.verify, hash, password)
        except VerifyMismatchError:
            # Password does not match hash — normal situation
            # Return False, do not log error
            return False
        except InvalidHash:
            # Hash has invalid format (corrupted or not Argon2)
            # Log error and return False
            logger.error(f"Invalid hash format: {hash}")
            return False
