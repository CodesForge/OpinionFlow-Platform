"""
FastAPI application entry point.

Main application configuration, lifespan management, and dependency injection setup.
"""

from fastapi import FastAPI
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from src.common.logger import logger
from src.infrastructure.di.providers import AppProvider
from src.infrastructure.messages.broker import KafkaMessageBroker
from src.infrastructure.db.config import DatabaseConfig
from src.presentation.api.routers.auth import router as auth_router


# ─────────────────────────────────────────────────────
# Application Lifespan
# ─────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles application startup and shutdown events:
    - Startup: Initialize DI container, connect to database
    - Shutdown: Close DI container, disconnect from database
    
    Args:
        app: FastAPI application instance.
        
    Yields:
        None: Control returns to FastAPI to handle requests.
    """
    # ─── Startup ─────────────────────────────────────
    logger.info("Starting up OpinionFlow API...")
    
    # Create DI container (APP scope)
    # This initializes all singleton dependencies
    container = app.state.dishka_container
    
    # Get database config and connect
    db_config = await container.get(DatabaseConfig)
    await db_config.connect()
    
    # Get broker config and connect
    broker = await container.get(KafkaMessageBroker)
    await broker.broker.connect()
    
    logger.info("Application startup complete")
    
    # Yield control to FastAPI (handle requests)
    yield
    
    # ─── Shutdown ─────────────────────────────────────
    logger.info("Shutting down OpinionFlow API...")
    
    # Disconnect from database
    await db_config.disconnect()
    
    # Disconnect from broker
    await broker.broker.stop()
    
    # Close DI container (cleanup REQUEST scope dependencies)
    await container.close()
    
    logger.info("Application shutdown complete")


# ─────────────────────────────────────────────────────
# Application Factory
# ─────────────────────────────────────────────────────
def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    
    Application configuration:
    - Title and description for Swagger UI
    - Lifespan events (startup/shutdown)
    - Dependency injection (Dishka)
    - API routers (auth, users, posts, etc.)
    - CORS middleware (if needed)
    - Health check endpoint
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    # Create FastAPI application
    app = FastAPI(
        title="OpinionFlow API",
        description="Social network API for opinions and polls",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",  # Swagger UI
        redoc_url="/redoc",  # ReDoc
    )
    
    # Create DI container and integrate with FastAPI
    # This makes dependencies available via FromDishka[]
    container = make_async_container(AppProvider())
    setup_dishka(container=container, app=app)
    
    # ─── Register Routers ──────────────────────────
    app.include_router(auth_router, prefix="/api/v1")
    
    # ─── Health Check ───────────────────────────────
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        """
        Health check endpoint.
        
        Returns:
            dict: Application status.
        """
        return {"status": "healthy", "version": "1.0.0"}
    
    return app


# ─────────────────────────────────────────────────────
# Application Instance
# ─────────────────────────────────────────────────────
app = create_app()