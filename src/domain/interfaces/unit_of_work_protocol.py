"""
Unit of Work protocol.

Interface for transactional boundary management.
"""

from typing import Protocol, TypeVar
from abc import abstractmethod

from src.domain.interfaces.repositories.user_repository_protocol import UserRepositoryProtocol
from src.infrastructure.db.repositories.user_repository import UserRepository


T = TypeVar('T')


class UnitOfWorkProtocol(Protocol):
    """
    Protocol for Unit of Work pattern implementation.
    
    Manages transactional boundaries and repository access.
    Ensures atomic operations across multiple repositories.
    
    Example usage:
        async with uow:
            user = uow.users.get_by_id(user_id)
            uow.users.add(user)
            await uow.commit()
    
    Attributes:
        users: User repository instance.
    """

    users: UserRepositoryProtocol

    async def __aenter__(self) -> 'UnitOfWorkProtocol':
        """
        Enters the unit of work context.
        
        Starts a new transaction.
        
        Returns:
            Self: Unit of Work instance.
        """
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exits the unit of work context.
        
        Commits transaction on success, rollbacks on error.
        
        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        """
        ...

    @abstractmethod
    async def commit(self) -> None:
        """
        Commits all pending changes in the transaction.
        
        Persists all changes made through repositories.
        """
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """
        Rollbacks all pending changes in the transaction.
        
        Discards all changes made through repositories.
        """
        ...
    @abstractmethod
    def repo(self) -> "UserRepository":
        """
        Returns the user repository instance.
        
        Provides access to user data operations within the unit of work.
        All repository operations participate in the same transaction.
        
        Returns:
            UserRepository: User repository instance.
        """
        ...
