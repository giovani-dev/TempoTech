"""
Módulo de repositório de conexão para PostgreSQL.

Este módulo gerencia a criação de sessões de banco de dados assíncronas para
o PostgreSQL, garantindo que as tabelas sejam criadas e que as sessões
sejam devidamente gerenciadas dentro de um contexto.
"""
import urllib
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from tempotech.core import config
from tempotech.core.interfaces.database_repository import IConnectionRepository


class ConnectionRepository(IConnectionRepository[AsyncSession]):
    """
    Repositório de conexão para o banco de dados PostgreSQL.

    Esta classe implementa a interface `IConnectionRepository` para fornecer
    uma conexão assíncrona com o banco de dados PostgreSQL.
    """

    @staticmethod
    async def connect() -> AsyncGenerator[AsyncSession, None]:
        """
        Cria e gerencia uma sessão de banco de dados assíncrona.

        Cria o motor assíncrono, garante que o esquema do banco de dados seja
        criado e, em seguida, cede uma sessão assíncrona para a aplicação.

        Yields:
            AsyncGenerator[AsyncSession, None]: Uma sessão de banco de dados assíncrona.
        """
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
    """
    Repositório de conexão aprimorado usando um gerenciador de contexto assíncrono.

    Esta versão da classe utiliza `asynccontextmanager` para um gerenciamento
    mais robusto e idiomático do ciclo de vida da sessão.
    """
    # Gambiarra para trabalhar com gerenciamento de contexto

    @staticmethod
    @asynccontextmanager
    async def connect() -> AsyncGenerator[AsyncSession, None]:
        """
        Cria e gerencia uma sessão de banco de dados assíncrona usando um
        gerenciador de contexto.

        Este método garante que a conexão e a sessão sejam abertas e fechadas
        automaticamente.

        Yields:
            AsyncGenerator[AsyncSession, None]: Uma sessão de banco de dados assíncrona.
        """
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