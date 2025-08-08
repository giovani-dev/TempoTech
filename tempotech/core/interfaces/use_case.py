"""
Módulo de interfaces para casos de uso.

Define o contrato básico para todos os casos de uso da aplicação.
Seguindo a arquitetura "Ports and Adapters", esta interface garante que a
lógica de negócio seja encapsulada e possa ser executada de forma consistente.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IUseCase(ABC, Generic[T]):
    """
    Interface para a execução de casos de uso.

    Esta interface genérica força que qualquer caso de uso tenha um
    método `execute` para encapsular e executar uma operação de negócio.
    """

    @abstractmethod
    async def execute(self) -> T:
        """
        Método abstrato para executar a lógica do caso de uso.

        A implementação deve conter a orquestração da lógica de negócios,
        retornando um resultado de tipo T.

        Returns:
            T: O resultado da execução do caso de uso.
        """
        pass
