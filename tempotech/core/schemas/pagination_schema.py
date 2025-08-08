"""
Módulo de esquemas de dados para paginação.

Define o modelo de dados Pydantic para encapsular uma resposta paginada.
Esse esquema é genérico e pode ser utilizado para paginar listas de
qualquer tipo de objeto, como, por exemplo, a lista de cidades ou
o histórico de consultas de clima.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    """
    Esquema de dados para uma resposta paginada.

    Encapsula os metadados de paginação (página atual, próxima e anterior,
    contagem de itens) e a lista de itens da página atual.
    """

    actual_page: int = Field(
        description="The number of the current page being displayed.",
        alias="actualPage",
        ge=0,
    )
    next_page: int = Field(
        description="The URL for the next page of results. It will be an empty string if there's no next page.",
        alias="nextPage",
    )
    previus_page: int = Field(
        description="The URL for the previous page of results. It will be an empty string if there's no previous page.",
        alias="previusPage",
    )
    items_count: int = Field(
        description="The number of items on the current page.",
        alias="itemsCount",
        ge=0,
    )
    items: list[T] = Field(
        description="A list containing the items for the current page."
    )
