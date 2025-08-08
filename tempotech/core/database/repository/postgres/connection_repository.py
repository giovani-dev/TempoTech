import urllib
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from tempotech.core import config
from tempotech.core.interfaces.database_repository import IConnectionRepository


class ConnectionRepository(IConnectionRepository[AsyncSession]):

    @staticmethod
    async def connect() -> AsyncGenerator[AsyncSession, None]:
        async_engine = create_async_engine(
            f"postgresql+asyncpg://{urllib.parse.quote(config.DB_USER)}:"
            + f"{urllib.parse.quote(config.DB_PWD)}@{config.DB_HOST}:"
            + f"{config.DB_PORT}/{config.DB_NAME}",
            echo=True,
        )
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        async_session = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session


class ConnectionRepositoryV2(IConnectionRepository[AsyncSession]):
    # Gambiarra para trabalhar com gerenciamento de contexto

    @staticmethod
    @asynccontextmanager
    async def connect() -> AsyncGenerator[AsyncSession, None]:
        async_engine = create_async_engine(
            f"postgresql+asyncpg://{urllib.parse.quote(config.DB_USER)}:"
            + f"{urllib.parse.quote(config.DB_PWD)}@{config.DB_HOST}:"
            + f"{config.DB_PORT}/{config.DB_NAME}",
            echo=True,
        )
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        async_session = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session
