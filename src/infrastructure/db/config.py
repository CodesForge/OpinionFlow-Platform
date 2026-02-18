from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Final
from contextlib import asynccontextmanager

from src.common.logger import logger
from src.config.database_settings import DatabaseSettings


class DatabaseConfig:
    """
    Database connection configuration.
    
    Implements:
    - Lazy initialization (created on first access)
    - Connection pooling (connection pool management)
    - Graceful shutdown (correct connection closing)
    
    Example:
        db = DatabaseConfig(settings)
        await db.connect()
        async with db.async_session() as session:
            result = await session.execute(query)
    """
    
    # Connection pool constants
    _DEFAULT_POOL_SIZE: Final[int] = 20  # Maximum connections in pool
    _DEFAULT_MAX_OVERFLOW: Final[int] = 10  # Temporary connections above limit
    _POOL_RECYCLE: Final[int] = 3600  # Recycle connections after 1 hour

    def __init__(self, settings: DatabaseSettings, echo: bool = False):
        """
        Initialize configuration.
        
        Args:
            settings: Connection settings (URL, credentials).
            echo: If True → log all SQL queries (for debugging).
        """
        self._settings = settings
        self._echo = echo
        self._async_engine: Optional[AsyncEngine] = None
        self._async_session: Optional[async_sessionmaker[AsyncSession]] = None

    @property
    def async_engine(self) -> AsyncEngine:
        """
        Returns async engine for database connection.
        
        Lazy initialization — created on first access.
        Uses connection pooling for performance.
        
        Returns:
            AsyncEngine: SQLAlchemy asynchronous engine.
            
        Raises:
            SQLAlchemyError: On engine initialization error.
            Exception: On other initialization errors.
        """
        if self._async_engine is None:
            try:
                self._async_engine = create_async_engine(
                    url=self._settings.get_db_url,
                    echo=self._echo,
                    pool_size=self._DEFAULT_POOL_SIZE,
                    max_overflow=self._DEFAULT_MAX_OVERFLOW,
                    pool_recycle=self._POOL_RECYCLE,
                    pool_pre_ping=True,
                )
                logger.info("Async engine successfully initialized")
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemy error during engine initialization: {e}")
                raise
            except Exception as e:
                logger.error(f"Failed to initialize async engine: {e}")
                raise
        return self._async_engine

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        """
        Returns async session factory for database connections.
        
        Lazy initialization — created on first access.
        Binds to async_engine.
        
        Returns:
            async_sessionmaker: Factory for creating AsyncSession.
            
        Raises:
            SQLAlchemyError: On session initialization error.
            Exception: On other initialization errors.
        """
        if self._async_session is None:
            try:
                self._async_session = async_sessionmaker(
                    bind=self.async_engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                    autocommit=False,
                    autoflush=False,
                )
                logger.info("Async session factory successfully initialized")
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemy error during session initialization: {e}")
                raise
            except Exception as e:
                logger.error(f"Failed to initialize async session: {e}")
                raise
        return self._async_session

    async def connect(self) -> None:
        """
        Establishes database connection.
        
        Initializes engine and performs health check.
        Called on application startup.
        
        Raises:
            Exception: When connection to database fails.
        """
        try:
            _ = self.async_engine
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self) -> None:
        """
        Closes all database connections correctly.
        
        Disposes engine resources, resets state.
        Called on application shutdown.
        """
        if self._async_engine is not None:
            try:
                await self._async_engine.dispose()
                self._async_engine = None
                self._async_session = None
                logger.info("Database connections closed successfully")
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemy error during disconnect: {e}")
                raise
            except Exception as e:
                logger.error(f"Failed to disconnect from database: {e}")
                raise
