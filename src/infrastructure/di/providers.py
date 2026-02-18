"""
Dependency Injection providers using Dishka.

Configures dependency injection container for the application.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, provide
from typing import AsyncGenerator

from src.infrastructure.security.authx_service import AuthxService
from src.config.authx_settings import get_authX_settings
from src.infrastructure.security.argon_service import ArgonService
from src.config.argon_service_settings import get_argon_settings
from src.infrastructure.db.config import DatabaseConfig
from src.config.database_settings import get_database_settings
from src.infrastructure.db.unit_of_work import UnitOfWork
from src.application.handlers.auth.register_user import RegisterUserHandler
from src.infrastructure.messages.broker import KafkaMessageBroker
from src.config.kafka_broker_settings import get_kafka_broker_settings


class AppProvider(Provider):
    """
    Dishka provider for application dependencies.
    
    Defines how to create and manage dependencies across the application.
    Uses scopes to control lifecycle:
    - APP: Singleton (created once, lives throughout app lifetime)
    - REQUEST: Created per request, disposed after request completes
    
    Registered dependencies:
    - DatabaseConfig (APP scope)
    - AuthxService (APP scope)
    - ArgonService (APP scope)
    - AsyncSession (REQUEST scope)
    - UnitOfWork (REQUEST scope)
    - RegisterUserHandler (REQUEST scope)
    """
    
    @provide(scope=Scope.APP)
    def get_db_config(self) -> DatabaseConfig:
        """
        Provides DatabaseConfig singleton instance.
        
        Creates DatabaseConfig once on application startup.
        Used for creating sessions and managing database connections.
        
        Returns:
            DatabaseConfig: Database configuration instance.
        """
        return DatabaseConfig(
            settings=get_database_settings(),
        )

    @provide(scope=Scope.APP)
    def get_kafka_broker(self) -> KafkaMessageBroker:
        """
        Provides KafkaMessageBroker singleton instance.

        Creates KafkaMessageBroker once on application startup.
        Used for publishing events to Kafka topics.
        
        Kafka broker is responsible for:
        - Publishing domain events to Kafka
        - Serializing events to JSON format
        - Managing Kafka connection and retries

        Returns:
            KafkaMessageBroker: Kafka message broker instance.
        """
        return KafkaMessageBroker(
            settings=get_kafka_broker_settings(),
        )

    @provide(scope=Scope.APP)
    def get_authx_service(self) -> AuthxService:
        """
        Provides AuthxService singleton instance.
        
        Creates AuthxService once on application startup.
        Used for JWT token generation and verification.
        
        Returns:
            AuthxService: JWT authentication service instance.
        """
        return AuthxService(
            settings=get_authX_settings(),
        )

    @provide(scope=Scope.APP)
    def get_argon_service(self) -> ArgonService:
        """
        Provides ArgonService singleton instance.
        
        Creates ArgonService once on application startup.
        Used for password hashing and verification.
        
        Returns:
            ArgonService: Password hashing service instance.
        """
        return ArgonService(
            settings=get_argon_settings(),
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, db: DatabaseConfig,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides AsyncSession per request.
        
        Creates a new database session for each request.
        Session is closed after request completes.
        This ensures proper connection management and isolation.
        
        Args:
            db: DatabaseConfig instance (injected from APP scope).
            
        Yields:
            AsyncSession: Database session for the request.
        """
        async with db.async_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_unit_of_work(
        self, db: DatabaseConfig,
    ) -> UnitOfWork:
        """
        Provides UnitOfWork per request.
        
        Creates a new UnitOfWork for each request.
        Manages transactional boundaries and repository access.
        Automatically commits on success, rollbacks on error.
        
        Args:
            db: DatabaseConfig instance (injected from APP scope).
            
        Returns:
            UnitOfWork: Unit of Work instance for transaction management.
        """
        return UnitOfWork(
            async_factory=db.async_session,
        )

    @provide(scope=Scope.REQUEST)
    def get_register_handler(
        self,
        uow: UnitOfWork,
        authx: AuthxService,
        hasher: ArgonService,
        broker: KafkaMessageBroker,
    ) -> RegisterUserHandler:
        """
        Provides RegisterUserHandler per request.
        
        Creates handler for user registration use case.
        Injects all required dependencies (UoW, AuthX, Argon).
        
        Args:
            uow: UnitOfWork instance (injected from REQUEST scope).
            authx: AuthxService instance (injected from APP scope).
            hasher: ArgonService instance (injected from APP scope).
            
        Returns:
            RegisterUserHandler: Handler for user registration.
        """
        return RegisterUserHandler(
            uow=uow, authx=authx, hasher=hasher, broker=broker,
        )
