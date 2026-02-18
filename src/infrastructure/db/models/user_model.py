"""
User database model.

SQLAlchemy model for user table storage.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Index
from datetime import datetime, timezone
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    Used as parent class for declarative model definition.
    """
    pass


class UserModel(Base):
    """
    User database model.
    
    Represents the 'user' table in PostgreSQL.
    Maps to User domain entity.
    
    Table columns:
        user_id: UUID primary key
        username: Unique username (max 15 chars)
        password: Argon2 hashed password
        created_at: Registration timestamp (UTC)
    
    Indexes:
        idx_user_username: Fast username lookup
        idx_user_created_at: Fast date-based queries
    """
    
    __tablename__ = "user"
    
    # ─────────────────────────────────────────────────────
    # Columns
    # ─────────────────────────────────────────────────────
    user_id: Mapped[str] = mapped_column(
        primary_key=True,
        index=True,  # Fast lookup by ID
        nullable=False,
    )
    
    username: Mapped[str] = mapped_column(
        String(15),  # Match Username._MAX_LEN
        unique=True,
        nullable=False,
        index=True,  # Fast login lookup
    )
    
    password: Mapped[str] = mapped_column(
        String(255),  # Argon2 hash length
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    # ─────────────────────────────────────────────────────
    # Table configuration
    # ─────────────────────────────────────────────────────
    __table_args__ = (
        Index("idx_user_username", "username"),
        Index("idx_user_created_at", "created_at"),
    )
    
