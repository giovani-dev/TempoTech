"""
Testes unitários para os esquemas de clima (`weather_schema.py`).

Este módulo contém testes para garantir que os modelos Pydantic `Temperature`
e `Weather` validam corretamente os dados de entrada, que seus atributos
são acessíveis conforme o esperado, e que a validação de `FutureDatetime`
funciona corretamente.
"""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from tempotech.core.schemas.weather_schema import (
    FutureDatetime,
    Temperature,
    Weather,
    ensure_future_datetime,
)


class TestEnsureFutureDatetimeUnit:
    """
    Classe de testes unitários para a função `ensure_future_datetime`.
    """

    def test_quando_datetime_futuro_entao_retorna_o_mesmo_datetime(self):
        """
        Verifica se a função retorna o datetime inalterado quando ele está no futuro.

        Cenário:
            Validação de um datetime que ocorre após o momento atual.

        Dado que:
            - Um objeto datetime que representa um momento no futuro.
        Quando:
            - A função `ensure_future_datetime` é chamada com esse datetime.
        Então:
            - A função retorna o mesmo objeto datetime sem levantar exceções.
        """
        # Dado que
        future_dt = datetime.now() + timedelta(seconds=1)

        # Quando
        result = ensure_future_datetime(future_dt)

        # Então
        assert result == future_dt

    def test_quando_datetime_passado_entao_levanta_assertion_error(self):
        """
        Verifica se a função levanta um AssertionError quando o datetime está no passado.

        Cenário:
            Validação de um datetime que ocorre antes do momento atual.

        Dado que:
            - Um objeto datetime que representa um momento no passado.
        Quando:
            - A função `ensure_future_datetime` é chamada com esse datetime.
        Então:
            - Um AssertionError é levantado, indicando que o datetime não é futuro.
        """
        # Dado que
        past_dt = datetime.now() - timedelta(seconds=1)

        # Quando/Então
        with pytest.raises(AssertionError):
            ensure_future_datetime(past_dt)


class TestTemperatureUnit:
    """
    Classe de testes unitários para o esquema `Temperature`.
    """

    def test_quando_temperatura_valida_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se um objeto Temperature é criado corretamente com dados válidos.

        Cenário:
            Criação bem-sucedida de um objeto Temperature com todas as temperaturas e unidade.

        Dado que:
            - Todas as temperaturas são números flutuantes válidos.
            - A unidade é "celsius".
        Quando:
            - Um objeto Temperature é instanciado com esses dados.
        Então:
            - O objeto é criado sem erros.
            - Os atributos correspondem aos valores fornecidos, incluindo o tratamento de aliases.
        """
        # Dado que
        valid_data = {
            "current": 25.5,
            "feelsLike": 26.0,
            "min": 20.0,
            "max": 30.0,
            "unit": "celsius",
        }

        # Quando
        temperature = Temperature(**valid_data)

        # Então
        assert temperature.current == 25.5
        assert temperature.feels_like == 26.0  # Verifica alias
        assert temperature.min == 20.0
        assert temperature.max == 30.0
        assert temperature.unit == "celsius"

    def test_quando_unidade_invalida_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando a unidade não é "celsius".

        Cenário:
            Tentativa de criar um objeto Temperature com uma unidade inválida.

        Dado que:
            - O campo 'unit' não é "celsius".
        Quando:
            - Um objeto Temperature é instanciado com esse dado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "current": 25.5,
            "feelsLike": 26.0,
            "min": 20.0,
            "max": 30.0,
            "unit": "fahrenheit",  # Unidade inválida
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Temperature(**invalid_data)

    def test_quando_temperatura_ausente_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando um campo de temperatura obrigatório está ausente.

        Cenário:
            Tentativa de criar um objeto Temperature sem o campo 'current' obrigatório.

        Dado que:
            - O campo 'current' é omitido.
        Quando:
            - Um objeto Temperature é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "feelsLike": 26.0,
            "min": 20.0,
            "max": 30.0,
            "unit": "celsius",
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Temperature(**invalid_data)


class TestWeatherUnit:
    """
    Classe de testes unitários para o esquema `Weather`.
    """

    def test_quando_clima_valido_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se um objeto Weather é criado corretamente com dados válidos.

        Cenário:
            Criação bem-sucedida de um objeto Weather com todos os campos preenchidos.

        Dado que:
            - Todos os campos são válidos, incluindo um objeto Temperature válido e um `timestamp_utc` futuro.
            - O país é "BR".
        Quando:
            - Um objeto Weather é instanciado com esses dados.
        Então:
            - O objeto é criado sem erros.
            - Os atributos correspondem aos valores fornecidos, incluindo o tratamento de aliases.
        """
        # Dado que
        valid_data = {
            "cityName": "São Paulo",
            "country": "BR",
            "temperature": {
                "current": 22.0,
                "feelsLike": 21.5,
                "min": 18.0,
                "max": 25.0,
                "unit": "celsius",
            },
            "humidity": 70,
            "windSpeed": 5.2,
            "timestampUtc": (datetime.now() + timedelta(minutes=1)).isoformat(),
        }

        # Quando
        weather = Weather(**valid_data)

        # Então
        assert weather.city_name == "São Paulo"  # Verifica alias
        assert weather.country == "BR"
        assert isinstance(weather.temperature, Temperature)
        assert weather.humidity == 70
        assert weather.wind_speed == 5.2  # Verifica alias
        assert isinstance(weather.timestamp_utc, datetime)  # Verifica FutureDatetime

    def test_quando_nome_da_cidade_muito_curto_entao_erro_de_validacao_e_retornado(
        self,
    ):
        """
        Verifica se um erro de validação é retornado quando o nome da cidade é muito curto.

        Cenário:
            Tentativa de criar um objeto Weather com um `city_name` que não atende ao `min_length`.

        Dado que:
            - O campo 'cityName' tem menos de 1 caractere.
        Quando:
            - Um objeto Weather é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "cityName": "",  # Muito curto
            "country": "BR",
            "temperature": {
                "current": 22.0,
                "feelsLike": 21.5,
                "min": 18.0,
                "max": 25.0,
                "unit": "celsius",
            },
            "humidity": 70,
            "windSpeed": 5.2,
            "timestampUtc": (datetime.now() + timedelta(minutes=1)).isoformat(),
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Weather(**invalid_data)

    def test_quando_pais_invalido_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando o país não é "BR".

        Cenário:
            Tentativa de criar um objeto Weather com um código de país inválido.

        Dado que:
            - O campo 'country' não é "BR".
        Quando:
            - Um objeto Weather é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "cityName": "Rio de Janeiro",
            "country": "US",  # País inválido
            "temperature": {
                "current": 22.0,
                "feelsLike": 21.5,
                "min": 18.0,
                "max": 25.0,
                "unit": "celsius",
            },
            "humidity": 70,
            "windSpeed": 5.2,
            "timestampUtc": (datetime.now() + timedelta(minutes=1)).isoformat(),
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Weather(**invalid_data)

    def test_quando_umidade_fora_do_intervalo_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando a umidade está fora do intervalo [0, 100].

        Cenário:
            Tentativa de criar um objeto Weather com um valor de umidade inválido.

        Dado que:
            - O campo 'humidity' é menor que 0 ou maior que 100.
        Quando:
            - Um objeto Weather é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data_low = {
            "cityName": "Curitiba",
            "country": "BR",
            "temperature": {
                "current": 15.0,
                "feelsLike": 14.0,
                "min": 10.0,
                "max": 20.0,
                "unit": "celsius",
            },
            "humidity": -5,  # Fora do intervalo
            "windSpeed": 3.0,
            "timestampUtc": (datetime.now() + timedelta(minutes=1)).isoformat(),
        }
        invalid_data_high = {
            "cityName": "Curitiba",
            "country": "BR",
            "temperature": {
                "current": 15.0,
                "feelsLike": 14.0,
                "min": 10.0,
                "max": 20.0,
                "unit": "celsius",
            },
            "humidity": 105,  # Fora do intervalo
            "windSpeed": 3.0,
            "timestampUtc": (datetime.now() + timedelta(minutes=1)).isoformat(),
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Weather(**invalid_data_low)
        with pytest.raises(ValidationError):
            Weather(**invalid_data_high)

    def test_quando_velocidade_do_vento_negativa_entao_erro_de_validacao_e_retornado(
        self,
    ):
        """
        Verifica se um erro de validação é retornado quando a velocidade do vento é negativa.

        Cenário:
            Tentativa de criar um objeto Weather com um valor de `windSpeed` inválido.

        Dado que:
            - O campo 'windSpeed' é um número negativo.
        Quando:
            - Um objeto Weather é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "cityName": "Porto Alegre",
            "country": "BR",
            "temperature": {
                "current": 20.0,
                "feelsLike": 19.0,
                "min": 15.0,
                "max": 22.0,
                "unit": "celsius",
            },
            "humidity": 60,
            "windSpeed": -1.0,  # Negativo
            "timestampUtc": (datetime.now() + timedelta(minutes=1)).isoformat(),
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Weather(**invalid_data)

    def test_quando_timestamp_utc_passado_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando o `timestamp_utc` está no passado.

        Cenário:
            Tentativa de criar um objeto Weather com um `timestamp_utc` que não é futuro.

        Dado que:
            - O campo 'timestampUtc' é um datetime no passado.
        Quando:
            - Um objeto Weather é instanciado.
        Então:
            - Uma exceção ValidationError é levantada devido à validação de `FutureDatetime`.
        """
        # Dado que
        invalid_data = {
            "cityName": "Belo Horizonte",
            "country": "BR",
            "temperature": {
                "current": 28.0,
                "feelsLike": 29.0,
                "min": 25.0,
                "max": 32.0,
                "unit": "celsius",
            },
            "humidity": 50,
            "windSpeed": 8.0,
            "timestampUtc": (
                datetime.now() - timedelta(minutes=1)
            ).isoformat(),  # Passado
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Weather(**invalid_data)

    def test_quando_timestamp_utc_com_formato_invalido_entao_erro_de_validacao_e_retornado(
        self,
    ):
        """
        Verifica se um erro de validação é retornado quando o `timestamp_utc` tem formato inválido.

        Cenário:
            Tentativa de criar um objeto Weather com um `timestamp_utc` que não é um datetime válido.

        Dado que:
            - O campo 'timestampUtc' é uma string com formato inválido.
        Quando:
            - Um objeto Weather é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "cityName": "Recife",
            "country": "BR",
            "temperature": {
                "current": 30.0,
                "feelsLike": 31.0,
                "min": 28.0,
                "max": 33.0,
                "unit": "celsius",
            },
            "humidity": 80,
            "windSpeed": 10.0,
            "timestampUtc": "invalid-date-format",  # Formato inválido
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Weather(**invalid_data)
