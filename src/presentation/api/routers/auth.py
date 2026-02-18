"""
Authentication API router.

Handles user authentication endpoints (register, login, logout).
"""

from fastapi import APIRouter, status, HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.presentation.api.schemas.user_schema import AuthUserResponseSchema, AuthUserSchema
from src.application.handlers.auth.register_user import RegisterUserHandler
from src.application.commands.auth.user_auth_command import UserAuthCommand
from src.domain.exceptions.domain import ValidationError
from src.domain.exceptions.user import UserAlreadyExistsError


# ─────────────────────────────────────────────────────
# Router Configuration
# ─────────────────────────────────────────────────────
router = APIRouter(
    prefix="/auth",  # All routes will be /auth/...
    tags=["Auth"],  # Groups endpoints in Swagger UI
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthUserResponseSchema,
    summary="Register a new user",
    description="Creates a new user account with the provided username and password.",
)
@inject
async def register_user(
    request: AuthUserSchema,
    handler: FromDishka[RegisterUserHandler],
) -> AuthUserResponseSchema:
    """
    Register a new user endpoint.
    
    This endpoint handles user registration by:
    1. Validating request data (username, password)
    2. Creating user command from request
    3. Executing registration handler
    4. Returning authentication result with access token
    
    Args:
        request: User registration data (username, password).
        handler: RegisterUserHandler injected via Dishka DI.
        
    Returns:
        AuthUserResponseSchema: Registration result with access token.
        
    Raises:
        HTTPException 400: If validation fails (username/password invalid).
        HTTPException 500: If unexpected error occurs.
        
    Example:
        POST /auth/register
        {
            "username": "alex",
            "password": "secure123"
        }
        
        Response 201:
        {
            "status": "success",
            "message": "User registered successfully",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    try:
        # Execute registration handler
        # Handler validates data, creates user, generates token
        return await handler.execute(
            cmd=UserAuthCommand(
                username=request.username,
                password=request.password,
            )
        )
    except ValidationError as e:
        # Validation failed (username/password invalid)
        # Return 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except UserAlreadyExistsError as e:
        # User with this username already exists
        # Return 400 Bad Request (conflict)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Unexpected error (database, service, etc.)
        # Return 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register the user: {e}",
        )
