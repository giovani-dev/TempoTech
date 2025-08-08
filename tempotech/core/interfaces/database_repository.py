from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class IConnectionRepository(ABC, Generic[T]):

    @staticmethod
    @abstractmethod
    def connect(host: str, port: str, user: str, pwd: str) -> T:
        pass


class IDefaultRepository(ABC, Generic[T]):

    @abstractmethod
    def create(self, data: T):
        pass

    @abstractmethod
    def update(self, data: T, id: int):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[T]:
        pass
