from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IUseCase(ABC, Generic[T]):
    @abstractmethod
    async def execute(self) -> T:
        pass
