"""
Unit of Work implementation.

SQLAlchemy-based transactional boundary management.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Optional, Self, Type
from types import TracebackType

from src.infrastructure.db.repositories.user_repository import UserRepository
from src.domain.interfaces.unit_of_work_protocol import UnitOfWorkProtocol


class UnitOfWork(UnitOfWorkProtocol):
    """
    SQLAlchemy implementation of Unit of Work pattern.
    
    Manages transactional boundaries and provides access to repositories.
    Ensures atomic operations — all changes commit together or rollback together.
    
    Features:
    - Context manager support (async with)
    - Automatic commit on success
    - Automatic rollback on error
    - Repository access within transaction
    
    Example usage:
        async with UnitOfWork(session_factory) as uow:
            user = await uow.users.get_by_id(user_id)
            uow.users.add(new_user)
            await uow.commit()
            
        # If exception occurs — automatic rollback
        # If no exception — automatic commit
    """
    
    def __init__(self, async_factory: async_sessionmaker[AsyncSession]) -> None:
        """
        Initialize Unit of Work.
        
        Args:
            async_factory: Async session factory for creating sessions.
        """
        self._async_factory = async_factory
        self._async_session: Optional[AsyncSession] = None
        self._repository: Optional[UserRepository] = None

    async def __aenter__(self) -> Self:
        """
        Enters the unit of work context.
        
        Creates a new async session and initializes repositories.
        Starts a new transaction implicitly.
        
        Returns:
            Self: Unit of Work instance for method chaining.
        """
        # Create new session for this unit of work
        self._async_session = self._async_factory()
        
        # Initialize repositories with the session
        # All repositories share the same session/transaction
        self._repository = UserRepository(self._async_session)
        
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        """
        Exits the unit of work context.
        
        Commits transaction if no exception occurred.
        Rollbacks transaction if exception occurred.
        Always closes the session.
        
        Args:
            exc_type: Exception type if raised (None if success).
            exc_val: Exception value if raised (None if success).
            exc_tb: Exception traceback if raised (None if success).
        """
        try:
            if self._async_session:
                if not exc_type:
                    # No exception — commit changes
                    await self._async_session.commit()
                else:
                    # Exception occurred — rollback changes
                    await self._async_session.rollback()
        finally:
            # Always close session (release connection back to pool)
            await self._async_session.close()

    async def commit(self) -> None:
        """
        Commits all pending changes in the transaction.
        
        Persists all changes made through repositories to database.
        Call this explicitly if not using context manager.
        """
        if self._async_session:
            await self._async_session.commit()

    async def rollback(self) -> None:
        """
        Rollbacks all pending changes in the transaction.
        
        Discards all changes made through repositories.
        Call this explicitly if you want to cancel changes.
        """
        if self._async_session:
            await self._async_session.rollback()

    @property
    def repo(self) -> UserRepository:
        """
        Returns the user repository instance.
        
        Provides access to user data operations within this unit of work.
        All operations use the same session and participate in the same transaction.
        
        Returns:
            UserRepository: User repository instance.
            
        Raises:
            RuntimeError: If called outside of context manager.
        """
        if self._repository is None:
            raise RuntimeError("UnitOfWork not initialized. Use 'async with' statement.")
        return self._repository
