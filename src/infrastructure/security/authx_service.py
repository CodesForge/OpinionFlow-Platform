"""
JWT authentication service using AuthX.

Production-ready JWT token management for authentication.
"""

from authx import AuthX, AuthXConfig
from datetime import timedelta
from typing import Optional

from src.common.logger import logger
from src.config.authx_settings import AuthX_Settings
from src.domain.interfaces.authx_service_protocol import AuthxServiceProtocol


class AuthxService(AuthxServiceProtocol):
    """
    JWT authentication service implementation.
    
    Provides token creation and verification using AuthX library.
    Supports access tokens with configurable expiration.
    
    Features:
    - Lazy initialization (config and AuthX created on first access)
    - Configurable token expiration
    - Secure JWT algorithms (HS256, RS256, etc.)
    
    Example:
        service = AuthxService(settings)
        token = service.create_access_token(uid="user_123")
        payload = service.verify_token(token)
    """
    
    def __init__(self, settings: AuthX_Settings):
        """
        Initialize JWT authentication service.
        
        Args:
            settings: JWT configuration parameters (secret, expiration, algorithm).
        """
        self._settings = settings
        self._authx: Optional[AuthX] = None
        self._config: Optional[AuthXConfig] = None

    @property
    def config(self) -> AuthXConfig:
        """
        Returns AuthXConfig instance with lazy initialization.
        
        Creates configuration on first access with settings from AuthX_Settings.
        Lazy init saves resources — created only when needed.
        
        Configuration includes:
        - JWT algorithm (HS256, RS256, etc.)
        - Token location (headers, cookies, etc.)
        - Access token expiration time
        - Secret key for signing
        
        Returns:
            AuthXConfig: Configured AuthX settings.
            
        Raises:
            Exception: If configuration initialization fails.
        """
        if self._config is None:
            try:
                # Create AuthXConfig with settings from config file
                self._config = AuthXConfig()
                self._config.JWT_ALGORITHM = self._settings.algorithm
                self._config.JWT_TOKEN_LOCATION = ["headers"]
                self._config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=self._settings.expires)
                self._config.JWT_SECRET_KEY = self._settings.secret_key
                logger.info("AuthXConfig initialized")
            except Exception as e:
                logger.error(f"Error in AuthXConfig initialization: {e}")
                raise
        return self._config

    @property
    def authx(self) -> AuthX:
        """
        Returns AuthX instance with lazy initialization.
        
        Creates AuthX on first access using configured settings.
        AuthX is the main class for JWT token operations.
        
        Returns:
            AuthX: Configured AuthX instance for token operations.
            
        Raises:
            Exception: If AuthX initialization fails.
        """
        if self._authx is None:
            try:
                # Create AuthX with config (lazy init)
                self._authx = AuthX(config=self.config)
                logger.info("AuthX initialized")
            except Exception as e:
                logger.error(f"Error in AuthX initialization: {e}")
                raise
        return self._authx

    async def create_access_token(self, uid: str) -> str:
        """
        Creates a new JWT access token for a user.
        
        Args:
            uid: Unique user identifier to encode in token.
            
        Returns:
            str: JWT access token (Bearer token).
            
        Raises:
            Exception: If token creation fails.
            
        Example:
            token = service.create_access_token(uid="user_123")
            # Return: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        """
        try:
            # Create access token with user ID
            # Token expires after JWT_ACCESS_TOKEN_EXPIRES (from config)
            return self.authx.create_access_token(uid=uid)
        except Exception as e:
            logger.error(f"Error in token creation: {e}")
            raise
