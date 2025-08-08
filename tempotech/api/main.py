"""
Módulo de entrada principal para a API TempoTech.

Este arquivo é o ponto de entrada da aplicação FastAPI. Ele gerencia o ciclo de vida
da aplicação, incluindo a inicialização do banco de dados e do Redis, além de
configurar e incluir os roteadores da API para localização e clima.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

from tempotech.api.router import location_router, weather_router
from tempotech.core import config
from tempotech.core.database.repository.postgres.connection_repository import (
    ConnectionRepositoryV2,
)
from tempotech.core.database.repository.postgres.location_repository import (
    LocationRepository,
)
from tempotech.core.providers import coutry_provider
from tempotech.core.use_case.create_location_use_case import CreateLocationUseCase

API_VERSION = "v1"


async def setup_db():
    """
    Inicializa o banco de dados e popula com dados iniciais.

    Esta função se conecta ao banco de dados, cria todas as tabelas e, em seguida,
    executa o caso de uso `CreateLocationUseCase` para buscar e persistir os
    estados e cidades de um provedor externo, como o IBGE.
    """
    async with ConnectionRepositoryV2.connect() as session:
        await CreateLocationUseCase(
            location_db=LocationRepository(session), location_provider=coutry_provider
        ).execute()


@asynccontextmanager
async def lifesplan(app: FastAPI) -> AsyncIterator[None]:
    """
    Gerenciador de ciclo de vida da aplicação FastAPI.

    Lida com os eventos de inicialização (startup) e desligamento (shutdown) da aplicação.
    - Na inicialização, cria uma tarefa em segundo plano para popular o banco de dados.
    - Conecta-se ao Redis para configurar o cache (`FastAPICache`) e a limitação de taxa
      (`FastAPILimiter`).
    - No desligamento, garante que as conexões sejam fechadas corretamente.

    Args:
        app (FastAPI): A instância da aplicação FastAPI.

    Yields:
        AsyncIterator[None]: Cede o controle para a aplicação, que irá rodar
        enquanto o contexto estiver ativo.
    """
    task = asyncio.create_task(setup_db())
    app.state.background_task = task

    redis = await aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifesplan)
"""
Instância principal da aplicação FastAPI.

A aplicação é configurada com um `lifespan` que gerencia a inicialização e o
desligamento de recursos externos. Os roteadores de `weather` e `location`
são incluídos para definir os endpoints da API.
"""
app.include_router(weather_router.router, prefix=f"/api/{API_VERSION}/weather")
app.include_router(location_router.router, prefix=f"/api/{API_VERSION}/location")


if __name__ == "__main__":
    uvicorn.run(app=app, port=8080)
