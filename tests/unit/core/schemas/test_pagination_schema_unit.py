"""
Testes unitários para o esquema de paginação (`pagination_schema.py`).

Este módulo contém testes para garantir que o modelo Pydantic `Pagination`
valida corretamente os dados de paginação e que seus atributos,
incluindo aliases, são acessíveis conforme o esperado.
"""

import pytest
from pydantic import ValidationError

from tempotech.core.schemas.pagination_schema import Pagination


class TestPaginationUnit:
    """
    Classe de testes unitários para o esquema `Pagination`.
    """

    def test_quando_dados_de_paginacao_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se um objeto Pagination é criado corretamente com dados válidos.

        Cenário:
            Criação bem-sucedida de um objeto Pagination com todos os campos preenchidos.

        Dado que:
            - Todos os campos de paginação (página atual, próxima, anterior, contagem de itens) são válidos.
            - A lista de itens é fornecida.
        Quando:
            - Um objeto Pagination é instanciado com esses dados.
        Então:
            - O objeto é criado sem erros.
            - Os atributos correspondem aos valores fornecidos, incluindo o tratamento de aliases.
        """
        # Dado que
        valid_data = {
            "actualPage": 1,
            "nextPage": 2,
            "previusPage": 0,
            "itemsCount": 10,
            "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
        }

        # Quando
        pagination = Pagination(**valid_data)

        # Então
        assert pagination.actual_page == 1  # Verifica alias
        assert pagination.next_page == 2  # Verifica alias
        assert pagination.previus_page == 0  # Verifica alias
        assert pagination.items_count == 10  # Verifica alias
        assert len(pagination.items) == 2
        assert pagination.items[0]["name"] == "Item 1"

    def test_quando_lista_de_itens_vazia_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se um objeto Pagination é criado corretamente com uma lista de itens vazia.

        Cenário:
            Criação bem-sucedida de um objeto Pagination sem itens.

        Dado que:
            - Todos os campos de paginação são válidos.
            - A lista de itens está vazia.
        Quando:
            - Um objeto Pagination é instanciado com esses dados.
        Então:
            - O objeto é criado sem erros.
            - A lista de itens está vazia.
        """
        # Dado que
        valid_data = {
            "actualPage": 5,
            "nextPage": 6,
            "previusPage": 4,
            "itemsCount": 0,
            "items": [],
        }

        # Quando
        pagination = Pagination(**valid_data)

        # Então
        assert pagination.actual_page == 5
        assert pagination.items_count == 0
        assert len(pagination.items) == 0

    def test_quando_pagina_atual_negativa_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando a página atual é negativa.

        Cenário:
            Tentativa de criar um objeto Pagination com um valor inválido para 'actualPage'.

        Dado que:
            - O campo 'actualPage' é um número negativo.
        Quando:
            - Um objeto Pagination é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "actualPage": -1,  # Inválido
            "nextPage": 0,
            "previusPage": -2,
            "itemsCount": 5,
            "items": [{"id": 1}],
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Pagination(**invalid_data)

    def test_quando_items_count_negativo_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando a contagem de itens é negativa.

        Cenário:
            Tentativa de criar um objeto Pagination com um valor inválido para 'itemsCount'.

        Dado que:
            - O campo 'itemsCount' é um número negativo.
        Quando:
            - Um objeto Pagination é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "actualPage": 1,
            "nextPage": 2,
            "previusPage": 0,
            "itemsCount": -1,  # Inválido
            "items": [{"id": 1}],
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Pagination(**invalid_data)

    def test_quando_items_nao_e_lista_entao_erro_de_validacao_e_retornado(self):
        """
        Verifica se um erro de validação é retornado quando 'items' não é uma lista.

        Cenário:
            Tentativa de criar um objeto Pagination com o campo 'items' de um tipo inválido.

        Dado que:
            - O campo 'items' é uma string em vez de uma lista.
        Quando:
            - Um objeto Pagination é instanciado.
        Então:
            - Uma exceção ValidationError é levantada.
        """
        # Dado que
        invalid_data = {
            "actualPage": 1,
            "nextPage": 2,
            "previusPage": 0,
            "itemsCount": 1,
            "items": "not a list",  # Inválido
        }

        # Quando/Então
        with pytest.raises(ValidationError):
            Pagination(**invalid_data)
