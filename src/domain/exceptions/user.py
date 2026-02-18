"""
User-specific exceptions.

Exceptions related to user operations and business rules.
"""


class UserAlreadyExistsError(Exception):
    """
    Exception raised when attempting to create a user that already exists.
    
    Used by repositories to signal duplicate user creation attempts.
    
    Attributes:
        message: Error message with the conflicting username.
    """
    
    def __init__(self, username: str):
        """
        Initialize user already exists error.
        
        Args:
            username: The username that already exists.
        """
        self.message = f"User with username '{username}' already exists"
        super().__init__(self.message)
