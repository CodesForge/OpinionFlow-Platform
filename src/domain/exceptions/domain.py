"""
Domain exceptions.

Base exceptions for domain layer errors.
"""


class DomainError(Exception):
    """
    Base exception for all domain errors.
    
    Raised when a domain rule is violated.
    """
    
    def __init__(self, message: str):
        """
        Initialize domain error.
        
        Args:
            message: Error message describing the domain violation.
        """
        super().__init__(message)


class ValidationError(DomainError):
    """
    Exception raised when validation fails.
    
    Used when a value object receives invalid data.
    """
    
    def __init__(self, message: str):
        """
        Initialize validation error.
        
        Args:
            message: Error message describing the validation failure.
        """
        super().__init__(message)
