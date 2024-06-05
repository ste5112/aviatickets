import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app import app
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from settings import app_settings


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        app_settings.postgresql_uri,
        future=True,
        echo=True,
        # https://stackoverflow.com/questions/75252097/fastapi-testing-runtimeerror-task-attached-to-a-different-loop
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_session(engine):
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    yield SessionLocal


@pytest_asyncio.fixture(scope="session")
async def client(db_session):
    with app.container._session_factory.override(db_session), TestClient(app) as client:
        yield client
