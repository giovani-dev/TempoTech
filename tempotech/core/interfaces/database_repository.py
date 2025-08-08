from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generic, Optional, TypeVar

T = TypeVar("T")


class IConnectionRepository(ABC, Generic[T]):

    @staticmethod
    @abstractmethod
    async def connect() -> AsyncGenerator[T, None]:
        pass


class IDefaultRepository(ABC, Generic[T]):

    @abstractmethod
    async def create(self, data: T):
        pass

    @abstractmethod
    async def update(self, data: T, id: int):
        pass

    @abstractmethod
    async def delete(self, id: int):
        pass

    @abstractmethod
    async def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[T]:
        pass
