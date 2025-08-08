"""
Módulo do caso de uso para criar e popular dados de localização.

Este módulo define a lógica para inicializar a base de dados de localização
com dados de um provedor externo. Ele verifica se os dados já existem no
banco e os insere caso não existam.
"""

from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location


class CreateLocationUseCase(IUseCase[None]):
    """
    Caso de uso para criar registros de localização no banco de dados.

    Orquestra a busca de estados e cidades de um provedor externo e, se não
    existirem no banco de dados local, os insere.
    """

    def __init__(
        self,
        location_db: IDefaultRepository[Location],
        location_provider: ILocationProvider,
    ):
        """
        Inicializa o caso de uso com o repositório de banco de dados e o provedor de localização.

        Args:
            location_db (IDefaultRepository[Location]): O repositório de banco de dados para persistir os dados.
            location_provider (ILocationProvider): O provedor de localização de onde os dados serão obtidos.
        """
        self._location_db = location_db
        self._location_provider = location_provider

    async def execute(self) -> None:
        """
        Executa a lógica de criação de dados de localização.

        Busca os estados do provedor, verifica a existência no banco de dados
        e, se necessário, busca as cidades do estado e as insere.
        """
        provider_data = self._location_provider.list_states()
        async for state in provider_data:
            local_data = await self._location_db.search(
                filters={
                    "country": self._location_provider.country,
                    "state": state.state,
                    "state_name": state.state_name,
                },
                limit=1,
            )
            if len(local_data) == 0:
                async for city in self._location_provider.list_cities_by_state(
                    state.state
                ):
                    await self._location_db.create(city)
