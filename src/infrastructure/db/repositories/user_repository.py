"""
User repository implementation.

SQLAlchemy-based repository for user data access.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select
from typing import Optional

from src.common.logger import logger
from src.domain.interfaces.repositories.user_repository_protocol import UserRepositoryProtocol
from src.domain.entities.user import User
from src.domain.value_objects.username import Username
from src.infrastructure.db.models.user_model import UserModel


class UserRepository(UserRepositoryProtocol):
    """
    SQLAlchemy implementation of UserRepositoryProtocol.
    
    Provides user data access operations.
    Uses async sessions for database access.
    
    Attributes:
        _async_factory: Async session factory.
    """
    
    def __init__(self, async_factory: AsyncSession) -> None:
        """
        Initialize user repository.
        
        Args:
            async_factory: Async session factory for database operations.
        """
        self._async_factory = async_factory

    async def add(self, user: User) -> None:
        """
        Adds a new user to the repository.
        
        Args:
            user: User entity to add.
            
        Raises:
            SQLAlchemyError: On database error.
            Exception: On unexpected error.
        """
        try:
            stmt = insert(UserModel).values({
                "user_id": str(user.user_id.value),
                "username": user.username.value,
                "password": user.password.value,
                "created_at": user.created_at,
            })
            await self._async_factory.execute(stmt)
            logger.info(
                f"User '@{user.username.value}' | '{str(user.user_id.value)}' was added successfully."
            )
        except SQLAlchemyError as e:
            logger.exception(
                f"SQLAlchemyError during user creation: {e}"
            )
            raise
        except Exception as e:
            logger.exception(
                f"Error during user creation '@{user.username.value}' | '{str(user.user_id.value)}': {e}"
            )
            raise
    
    async def get_by_username(self, username: Username) -> Optional[User]:
        """
        Retrieves a user by their username.

        Executes a SELECT query on the user table filtering by username.
        Returns None if user is not found.

        Args:
            username: Username string to search for.

        Returns:
            Optional[User]: User entity if found, None otherwise.

        Raises:
            SQLAlchemyError: On database error.
            Exception: On unexpected error.

        Example:
            user = await repository.get_by_username("alex")
            if user:
                print(f"Found user: {user.username}")
            else:
                print("User not found")
        """
        try:
            # Build SELECT query filtering by username
            # scalar_one_or_none() returns single result or None
            return (await self._async_factory.execute(
                select(UserModel).where(
                    UserModel.username == username,
                )
            )).scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError in get_by_username: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in get_by_username: {e}")
            raise
            