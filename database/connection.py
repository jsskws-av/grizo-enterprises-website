"""
Database Connection & Session Factory
Configures SQLite in WAL (Write-Ahead Logging) mode for high-concurrency read/write operations.
Supports both asynchronous (FastAPI routes) and synchronous (CLI/cron jobs) sessions.
"""

import os
import sqlite3
from typing import AsyncGenerator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.settings import DB_PATH, DATABASE_URL, SYNC_DATABASE_URL
from database.models import Base

# Ensure SQLite directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Synchronous Engine (used for initial table creation, migrations, and synchronous tests)
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

# Enable WAL Mode and Foreign Keys on SQLite connections
@event.listens_for(sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Asynchronous Engine (for async FastAPI endpoints)
async_engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def init_db():
    """Create all tables in SQLite database synchronously."""
    Base.metadata.create_all(bind=sync_engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Session:
    """Helper for synchronous background operations."""
    db = SyncSessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise
