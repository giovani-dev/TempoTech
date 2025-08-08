"""
Testes de integração para o caso de uso `SearchCity`.

Este módulo contém testes que verificam a interação entre o caso de uso `SearchCity`
e sua dependência `IDefaultRepository`, simulando um cenário mais próximo
da realidade, mas ainda utilizando mocks para as implementações concretas
da interface do repositório.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination
from tempotech.core.use_case.search_city_use_case import SearchCity


class TestSearchCityIntegration:
    """
    Classe de testes de integração para o caso de uso `SearchCity`.
    """

    @pytest.mark.asyncio
    async def test_quando_repositorio_de_localizacao_e_integrado_corretamente_entao_cidades_sao_paginadas(
        self,
    ):
        """
        Verifica a integração entre o caso de uso e o repositório de localização para paginação.

        Cenário:
            O caso de uso `SearchCity` interage corretamente com uma implementação
            (mockada) de `IDefaultRepository` para buscar e paginar cidades.

        Dado que:
            - Uma implementação mockada de `IDefaultRepository` que retorna uma lista de cidades.
        Quando:
            - O caso de uso `SearchCity` é instanciado com essa implementação e parâmetros de paginação.
            - O método `execute` do caso de uso é chamado.
        Então:
            - O caso de uso retorna um objeto `Pagination` com as cidades e metadados corretos.
            - O método `search` da implementação do repositório é invocado com os argumentos esperados.
        """
        # Dado que
        mock_repo_instance = MagicMock(spec=IDefaultRepository)
        mock_repo_instance.search.return_value = [
            Location(
                country="BR", state="SP", stateName="São Paulo", cityName="São Paulo"
            ),
            Location(
                country="BR", state="SP", stateName="São Paulo", cityName="Campinas"
            ),
            Location(
                country="BR",
                state="SP",
                stateName="São Paulo",
                cityName="Ribeirão Preto",
            ),
        ]

        use_case = SearchCity(
            location_db=mock_repo_instance, state="SP", page=1, page_size=10
        )

        # Quando
        result = await use_case.execute()

        # Então
        assert isinstance(result, Pagination)
        assert result.actual_page == 1
        assert result.items_count == 3
        assert result.items[0].city_name == "São Paulo"
        mock_repo_instance.search.assert_called_once_with(
            filters={"state": "SP"}, offset=0, limit=10
        )

    @pytest.mark.asyncio
    async def test_quando_repositorio_de_localizacao_e_integrado_com_filtro_entao_cidades_filtradas_sao_retornadas(
        self,
    ):
        """
        Verifica a integração entre o caso de uso e o repositório de localização com filtros.

        Cenário:
            O caso de uso `SearchCity` interage corretamente com uma implementação
            (mockada) de `IDefaultRepository` para buscar cidades com um filtro.

        Dado que:
            - Uma implementação mockada de `IDefaultRepository` que retorna cidades filtradas.
        Quando:
            - O caso de uso `SearchCity` é instanciado com essa implementação e parâmetros de filtro.
            - O método `execute` do caso de uso é chamado.
        Então:
            - O caso de uso retorna um objeto `Pagination` com as cidades filtradas.
            - O método `search` da implementação do repositório é invocado com os argumentos de filtro esperados.
        """
        # Dado que
        mock_repo_instance = MagicMock(spec=IDefaultRepository)
        mock_repo_instance.search.return_value = [
            Location(
                country="BR", state="RJ", stateName="Rio de Janeiro", cityName="Niterói"
            ),
        ]

        use_case = SearchCity(
            location_db=mock_repo_instance,
            state="RJ",
            search_by="city_name",
            search_value="Niterói",
            page=1,
            page_size=10,
        )

        # Quando
        result = await use_case.execute()

        # Então
        assert isinstance(result, Pagination)
        assert result.items_count == 1
        assert result.items[0].city_name == "Niterói"
        mock_repo_instance.search.assert_called_once_with(
            filters={"state": "RJ", "city_name": "Niterói"}, offset=0, limit=10
        )
