"""
Testes unitários para os esquemas de localização (`location_schema.py`).

Este módulo contém testes para garantir que os modelos Pydantic `Coordinates`
e `Location` validam corretamente os dados de entrada e que seus atributos
são acessíveis conforme o esperado.
"""

import pytest
from pydantic import ValidationError

from tempotech.core.schemas.location_schema import Coordinates, Location


class TestCoordinatesUnit:
    """
    Classe de testes unitários para o esquema `Coordinates`.
    """

    def test_quando_coordenadas_validas_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se um objeto Coordinates é criado corretamente com dados válidos.

        Cenário:
            Criação bem-sucedida de um objeto Coordinates com latitude e longitude válidas.

        Dado que:
            - Latitude e longitude são números flutuantes válidos.
        Quando:
            - Um objeto Coordinates é instanciado com esses dados.
        Então:
            - O objeto é criado sem erros.
            - Os atributos latitude e longitude correspondem aos valores fornecidos.
        """
        # Dado que
        valid_data = {"latitude": 40.7128, "longitude": -74.0060}

        # Quando
        coordinates = Coordinates(**valid_data)

        # Então
        assert coordinates.latitude == 40.7128
        assert coordinates.longitude == -74.0060

    def test_quando_coordenadas_nulas_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se um objeto Coordinates é criado corretamente com latitude e longitude nulas (opcionais).

        Cenário:
            Criação bem-sucedida de um objeto Coordinates sem fornecer latitude e longitude.

        Dado que:
            - Nenhum valor é fornecido para latitude e longitude (são opcionais).
        Quando:
            - Um objeto Coordinates é instanciado sem esses dados.
        Então:
            - O objeto é criado sem erros.
            - Os atributos latitude e longitude são None.
        """
        # Dado que
        valid_data = {}

        # Quando
        coordinates = Coordinates(**valid_data)

        # Então
        assert coordinates.latitude is None
        assert coordinates.longitude is None


class TestLocationUnit:
    """
    Classe de testes unitários para o esquema `Location`.
    """

    def test_quando_localizacao_valida_com_cidade_entao_objeto_e_criado_com_sucesso(
        self,
    ):
        """
        Verifica se um objeto Location é criado corretamente com todos os dados válidos, incluindo cidade e coordenadas.

        Cenário:
            Criação bem-sucedida de um objeto Location com todos os campos preenchidos.

        Dado que:
            - Todos os campos obrigatórios e opcionais (incluindo Coordinates) são válidos.
            - O país é "BR".
        Quando:
            - Um objeto Location é instanciado com esses dados.
        Então:
            - O objeto é criado sem erros.
            - Os atributos correspondem aos valores fornecidos, incluindo o tratamento de aliases.
        """
        # Dado que
        valid_data = {
            "country": "BR",
            "state": "SC",
            "stateName": "Santa Catarina",
            "cityName": "Florianópolis",
            "coordinates": {"latitude": -27.5935, "longitude": -48.5588},
        }

        # Quando
        location = Location(**valid_data)

        # Então
        assert location.country == "BR"
        assert location.state == "SC"
        assert location.state_name == "Santa Catarina"  # Verifica alias
        assert location.city_name == "Florianópolis"  # Verifica alias
        assert isinstance(location.coordinates, Coordinates)
        assert location.coordinates.latitude == -27.5935
        assert location.coordinates.longitude == -48.5588

    def test_quando_localizacao_valida_sem_cidade_entao_objeto_e_criado_com_sucesso(
        self,
    ):
        """
        Verifica se um objeto Location é criado corretamente para um estado (sem cidade).

        Cenário:
            Criação bem-sucedida de um objeto Location representando apenas um estado.

        Dado que:
            - Campos de cidade e coordenadas são omitidos (são opcionais).
            - O país é "BR".
        Quando:
            - Um objeto Location é instanciado com dados apenas de estado.
        Então:
            - O objeto é criado sem erros.
            - Os atributos de cidade e coordenadas são None.
        """
        # Dado que
        valid_data = {
            "country": "BR",
            "state": "SP",
            "stateName": "São Paulo",
        }

        # Quando
        location = Location(**valid_data)

        # Então
        assert location.country == "BR"
        assert location.state == "SP"
        assert location.state_name == "São Paulo"
        assert location.city_name is None
        assert location.coordinates is None

    def test_quando_pais_invalido_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando o país não é "BR".

        Cenário:
            Tentativa de criar um objeto Location com um código de país inválido.

        Dado que:
            - O campo 'country' não é "BR".
        Quando:
            - Um objeto Location é instanciado com esse dado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "country": "US",  # País inválido
            "state": "CA",
            "stateName": "California",
            "cityName": "Los Angeles",
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Location(**invalid_data)

    def test_quando_state_ausente_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando o campo 'state' está ausente.

        Cenário:
            Tentativa de criar um objeto Location sem o campo 'state' obrigatório.

        Dado que:
            - O campo 'state' é omitido.
        Quando:
            - Um objeto Location é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "country": "BR",
            "stateName": "Rio de Janeiro",
            "cityName": "Rio de Janeiro",
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Location(**invalid_data)

    def test_quando_state_name_ausente_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando o campo 'stateName' está ausente.

        Cenário:
            Tentativa de criar um objeto Location sem o campo 'stateName' obrigatório.

        Dado que:
            - O campo 'stateName' é omitido.
        Quando:
            - Um objeto Location é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "country": "BR",
            "state": "RJ",
            "cityName": "Rio de Janeiro",
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Location(**invalid_data)

    def test_quando_coordenadas_invalidas_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando as coordenadas são de tipo inválido.

        Cenário:
            Tentativa de criar um objeto Location com coordenadas que não são um dicionário ou objeto Coordinates.

        Dado que:
            - O campo 'coordinates' é um tipo inválido (ex: string).
        Quando:
            - Um objeto Location é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "country": "BR",
            "state": "SC",
            "stateName": "Santa Catarina",
            "cityName": "Blumenau",
            "coordinates": "invalid_coordinates",  # Coordenadas inválidas
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Location(**invalid_data)
