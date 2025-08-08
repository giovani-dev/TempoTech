"""
Módulo de injeção de dependência para conexão e repositórios de banco de dados.

Este módulo centraliza a lógica de injeção de dependência (DI) para interações
com o banco de dados. Ele define a sessão de banco de dados e o repositório de
localização como dependências reutilizáveis para os endpoints da API,
promovendo a separação de responsabilidades e a testabilidade.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine

from tempotech.core.database.repository import LocationRepository
from tempotech.core.database.repository.postgres.connection_repository import (
    ConnectionRepository,
)
from tempotech.core.interfaces.database_repository import (
    IConnectionRepository,
    IDefaultRepository,
)
from tempotech.core.schemas.location_schema import Location

DbSession = Annotated[
    IConnectionRepository[Engine], Depends(ConnectionRepository.connect)
]
"""
Type alias que representa a dependência de uma sessão de banco de dados.

Utiliza `Annotated` para injetar uma conexão de repositório,
garantindo que uma nova sessão seja criada e gerenciada
a cada requisição de endpoint que a utiliza.
"""


def get_location_repository(session: DbSession) -> IDefaultRepository[Location]:
    """
    Função de injeção de dependência que fornece o repositório de localização.

    Args:
        session (DbSession): A sessão de banco de dados injetada.

    Returns:
        IDefaultRepository[Location]: Uma instância do repositório de localização.
    """
    return LocationRepository(session=session)


LocationDbRepository = Annotated[
    IDefaultRepository[Location], Depends(get_location_repository)
]
"""
Type alias que representa a dependência do repositório de localização.

Quando injetado em um endpoint, FastAPI chamará `get_location_repository` para
fornecer uma instância do repositório, permitindo a interação com os dados de
localização no banco de dados.
"""
