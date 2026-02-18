"""
Register user command handler.

Handles user registration use case with proper transaction management.
"""

from src.domain.exceptions.user import UserAlreadyExistsError
from src.domain.interfaces.argon_service_protocol import ArgonServiceProtocol
from src.domain.interfaces.authx_service_protocol import AuthxServiceProtocol
from src.domain.interfaces.unit_of_work_protocol import UnitOfWorkProtocol
from src.domain.interfaces.kafka_broker_protocol import KafkaBrokerProtocol
from src.application.commands.auth.user_auth_command import UserAuthCommand
from src.application.dto.auth.auth_result_dto import AuthResultDto
from src.domain.value_objects.username import Username
from src.domain.entities.user import User

class RegisterUserHandler:
    """
    Handler for user registration use case.
    
    Implements the application layer logic for registering a new user.
    Coordinates between domain entities, repositories, and infrastructure services.
    
    Responsibilities:
    - Validate command data (via domain entities)
    - Create user entity with hashed password
    - Persist user to database (transactional)
    - Generate JWT access token
    - Return authentication result
    
    Dependencies:
    - UnitOfWork: Transactional boundary management
    - AuthxService: JWT token generation
    - ArgonService: Password hashing
    
    Example:
        handler = RegisterUserHandler(uow, authx, hasher)
        result = await handler.execute(UserAuthCommand(username="alex", password="secure123"))
    """
    
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        authx: AuthxServiceProtocol,
        hasher: ArgonServiceProtocol,
        broker: KafkaBrokerProtocol,
    ) -> None:
        """
        Initialize register user handler.
        
        Args:
            uow: Unit of Work for transaction management.
            authx: AuthX service for JWT token generation.
            hasher: Argon2 service for password hashing.
        """
        self._uow = uow
        self._authx = authx
        self._hasher = hasher
        self._broker = broker

    async def execute(self, cmd: UserAuthCommand) -> AuthResultDto:
        """
        Executes the user registration use case.
        
        Process flow:
        1. Start unit of work (transaction)
        2. Create user entity (validates username/password, hashes password)
        3. Add user to repository
        4. Commit transaction (or rollback on error)
        5. Generate JWT access token
        6. Return authentication result
        
        Args:
            cmd: User registration command with username and password.
            
        Returns:
            AuthResultDto: Registration result with access token.
            
        Raises:
            ValidationError: If username or password validation fails.
            UserAlreadyExistsError: If username is already taken.
            Exception: On unexpected errors.
            
        Example:
            result = await handler.execute(
                UserAuthCommand(username="alex", password="secure123")
            )
            # result.status = "success"
            # result.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        """
        # Start unit of work (transaction)
        # All operations within this block are atomic
        # If any operation fails — entire transaction is rolled back
        async with self._uow:
            # Check if username already exists
            # This prevents duplicate usernames in the database
            user_by_username = await self._uow.repo.get_by_username(
                username=cmd.username,
            )
            if user_by_username:
                # Username is taken — raise conflict error
                raise UserAlreadyExistsError(
                    username=cmd.username,
                )

            # Create user entity
            # This validates username/password and hashes the password
            # Domain logic is encapsulated in User.create()
            # Returns User entity with hashed password and domain events
            user = await User.create(
                raw_username=cmd.username,
                plain_password=cmd.password,
                hasher=self._hasher,
            )

            # Add user to repository (within transaction)
            # Will be committed when exiting the context manager
            # If exception occurs — automatically rolled back
            await self._uow.repo.add(user)

            # If no exception — commit automatically
            # If exception — rollback automatically

        # Generate JWT access token for the new user
        # This is outside the transaction (infrastructure concern)
        access_token = await self._authx.create_access_token(
            uid=str(user.user_id.value)
        )

        # Publish domain events to Kafka
        # This notifies other services about user registration
        # Events are pulled from the user aggregate
        events = user.pull_events()
        for event in events:
            await self._broker.publish(
                topic="user_events",
                event=event.to_dict(),
            )

        # Return authentication result
        return AuthResultDto(
            status="success",
            message="User registered successfully",
            access_token=access_token,
        )
