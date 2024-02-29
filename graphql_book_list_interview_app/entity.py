import dataclasses
import typing

import strawberry

import graphql_book_list_interview_app.constant as constant


@strawberry.type
class Author:
    id: int
    name: str


@strawberry.type
class Book:
    id: int
    title: str
    author: Author


@dataclasses.dataclass(slots=True)
class BookFilters:
    author_ids: list[int] | None = None
    search: str | None = None


@dataclasses.dataclass(slots=True)
class PaginationConfig:
    limit: int = constant.MAX_PER_PAGE
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit > constant.MAX_PER_PAGE:
            raise ValueError(self.limit)


Item = typing.TypeVar("Item")


@strawberry.type
class PaginationWindow(typing.Generic[Item]):
    items: list[Item]
    total: int
