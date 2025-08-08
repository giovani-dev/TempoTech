"""
Módulo de inicialização do repositório de banco de dados.

Este módulo lida com a configuração e inicialização dos repositórios de banco de dados
com base no motor de banco de dados especificado nas configurações da aplicação.
Atualmente, ele suporta a configuração para PostgreSQL, importando os repositórios
apropriados para este motor.
"""

from tempotech.core import config

if config.DB_ENGINE == "POSTGRESQL":
    from tempotech.core.database.repository.postgres.connection_repository import (
        ConnectionRepository,
    )
    from tempotech.core.database.repository.postgres.location_repository import (
        LocationRepository,
    )
