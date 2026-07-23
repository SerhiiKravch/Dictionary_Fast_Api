from __future__ import annotations

import os
import time
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from alembic.config import Config
from app.core.db import Base, get_db
from app.main import app

POSTGRES_TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+psycopg://dictionary_user:dictionary_pass@localhost:5434/dictionary_test",
)


def wait_for_postgres(database_url: str, attempts: int = 20, delay: float = 1.0) -> None:
    engine = create_engine(database_url, future=True, pool_pre_ping=True)
    try:
        for attempt in range(attempts):
            try:
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                return
            except OperationalError:
                if attempt == attempts - 1:
                    raise
                time.sleep(delay)
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def postgres_engine():
    wait_for_postgres(POSTGRES_TEST_DATABASE_URL)

    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", POSTGRES_TEST_DATABASE_URL)
    command.upgrade(alembic_config, "head")

    engine = create_engine(POSTGRES_TEST_DATABASE_URL, future=True, pool_pre_ping=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def postgres_session_factory(postgres_engine):
    return sessionmaker(
        bind=postgres_engine,
        autoflush=False,
        autocommit=False,
        class_=Session,
    )


@pytest.fixture(autouse=True)
def cleanup_postgres_tables(postgres_engine) -> Generator[None, None, None]:
    yield

    table_names = [table.name for table in reversed(Base.metadata.sorted_tables)]
    joined_names = ", ".join(table_names)
    with postgres_engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {joined_names} RESTART IDENTITY CASCADE"))


@pytest.fixture
def postgres_db_session(postgres_session_factory) -> Generator[Session, None, None]:
    db = postgres_session_factory()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def postgres_client(postgres_db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield postgres_db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
