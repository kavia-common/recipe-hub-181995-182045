"""
Database setup for the FastAPI app using SQLAlchemy and SQLite.

This module exposes:
- engine: SQLAlchemy engine
- SessionLocal: session factory
- Base: declarative base for ORM models
- get_db: FastAPI dependency to get a scoped DB session per request
- init_db: function to create all tables (called in app startup)

Environment:
- Uses SQLITE_DB_URL from .env if provided; otherwise defaults to sqlite:///./recipes.db
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from dotenv import load_dotenv

# Load environment variables without hardcoding secrets in code
load_dotenv()

DEFAULT_SQLITE_URL = "sqlite:///./recipes.db"
DATABASE_URL = os.getenv("SQLITE_DB_URL", DEFAULT_SQLITE_URL)


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy ORM models."""


# For SQLite, check_same_thread must be False when used with multiple threads (e.g., FastAPI)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

# Session factory; autocommit/flush disabled, autoflush False to control flush points
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


# PUBLIC_INTERFACE
def init_db() -> None:
    """Create database tables based on ORM models."""
    # Import models so they register with Base.metadata
    from .models import recipe, tag, ingredient, recipe_tag  # noqa: F401
    Base.metadata.create_all(bind=engine)


# PUBLIC_INTERFACE
def get_db() -> Generator:
    """Yield a database session for the request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
