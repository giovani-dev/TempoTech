"""
Módulo do caso de uso para buscar estados.

Este módulo define a lógica de negócio para buscar uma lista de estados
usando um provedor de localização externo. Ele encapsula a orquestração
entre o provedor e a resposta da aplicação.
"""
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location


class SearchState(IUseCase[list[Location]]):
    """
    Caso de uso para buscar e retornar uma lista de estados.

    Orquestra a busca de estados através de um `ILocationProvider` e
    retorna os resultados como uma lista de objetos `Location`.
    """
    def __init__(
        self,
        location_provider: ILocationProvider,
    ):
        """
        Inicializa o caso de uso com um provedor de localização.

        Args:
            location_provider (ILocationProvider): O provedor de dados de localização a ser utilizado.
        """
        self._location_provider = location_provider

    async def execute(self) -> list[Location]:
        """
        Executa o caso de uso para obter todos os estados do provedor.

        Returns:
            list[Location]: Uma lista de objetos `Location` representando os estados.
        """
        return [item async for item in self._location_provider.list_states()]