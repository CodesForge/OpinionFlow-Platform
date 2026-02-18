"""
User repository protocol.

Interface for user data access operations.
"""

from typing import Protocol, Optional, List
from abc import abstractmethod

from src.domain.entities.user import User
from src.domain.value_objects.user_id import UserID
from src.domain.value_objects.username import Username


class UserRepositoryProtocol(Protocol):
    """
    Protocol for User repository implementation.

    Defines the interface for user data access operations.
    Follows repository pattern for data abstraction.

    Example usage:
        user = await user_repository.get_by_id(user_id)
        user = await user_repository.get_by_username(username)
        await user_repository.add(user)
        await user_repository.remove(user_id)
    """

    @abstractmethod
    async def add(self, user: User) -> None:
        """
        Adds a new user to the repository.
        
        Args:
            user: User entity to add.
            
        Raises:
            UserAlreadyExistsError: If user already exists.
        """
        ...
    
    @abstractmethod
    async def get_by_username(self, username: Username) -> Optional[User]:
        """
        Retrieves a user by their username.

        Args:
            username: Username value object to search for.

        Returns:
            Optional[User]: User if found, None otherwise.
        """
        ...