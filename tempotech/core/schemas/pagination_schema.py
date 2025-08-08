from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    actual_page: int = Field(
        description="The number of the current page being displayed.",
        alias="actualPage",
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
        description="The number of items on the current page.", alias="itemsCount"
    )
    items: list[T] = Field(
        description="A list containing the items for the current page."
    )
