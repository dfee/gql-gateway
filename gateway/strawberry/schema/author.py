from enum import Enum
from typing import Iterable, List, Optional

import strawberry

from gateway.client.author import (
    AuthorDto,
    AuthorQueryDto,
    AuthorSortByDto,
    AuthorSortDto,
)
from gateway.client.book import BookDto
from gateway.context import Context

from ..info import Info
from ._lazy import LazyBook, LazyPageInfo
from .node import Node
from .page import SortOrder

__all__ = [
    "Author",
    "AuthorSortInput",
    "AuthorSortBy",
    "AuthorConnection",
    "AuthorQueryInput",
    "AuthorConnection",
]


def resolve_books(root: AuthorDto, info: Info) -> Iterable[BookDto]:
    return info.context.dataloaders.books_by_author_id.load(root.id)


def resolve_full_name(root: AuthorDto) -> str:
    return f"{root.first_name} {root.last_name}"


@strawberry.type
class Author(Node):
    first_name: str
    full_name: str = strawberry.field(resolver=resolve_full_name)
    last_name: str
    books: List[LazyBook] = strawberry.field(resolver=resolve_books)

    @classmethod
    def is_type_of(cls, obj, _info) -> bool:
        return isinstance(obj, AuthorDto)


@strawberry.enum
class AuthorSortBy(Enum):
    CREATED_AT = "created_at"
    FIRST_NAME = "first_name"

    def to_dto(self) -> AuthorSortByDto:
        return AuthorSortByDto(self.value)

    @classmethod
    def from_dto(cls: "AuthorSortBy", dto: AuthorSortByDto) -> "AuthorSortBy":
        return cls(dto.value)


@strawberry.input
class AuthorSortInput:
    by: AuthorSortBy
    order: SortOrder

    def to_dto(self) -> AuthorSortDto:
        return AuthorSortDto(
            by=self.by.to_dto(),
            order=self.order.to_dto(),
        )

    @classmethod
    def from_dto(cls: "AuthorSortInput", dto: AuthorSortDto) -> "AuthorSortInput":
        return cls(
            by=AuthorSortBy.from_dto(dto.by),
            order=SortOrder.from_dto(dto.order),
        )


@strawberry.input
class AuthorQueryInput:
    after: Optional[str] = strawberry.field(default=None)
    before: Optional[str] = strawberry.field(default=None)
    first: Optional[int] = strawberry.field(default=None)
    last: Optional[int] = strawberry.field(default=None)
    sorts: Optional[List[AuthorSortInput]] = strawberry.field(default_factory=list)

    def to_dto(self) -> AuthorQueryDto:
        return AuthorQueryDto(
            after=self.after,
            before=self.before,
            first=self.first,
            last=self.last,
            sorts=[sort.to_dto() for sort in self.sorts],
        )

    @classmethod
    def from_dto(cls: "AuthorQueryInput", dto: AuthorQueryDto) -> "AuthorQueryInput":
        return cls(
            after=dto.after,
            before=dto.before,
            first=dto.first,
            last=dto.last,
            sorts=[AuthorSortInput.from_dto(sort) for sort in dto.sorts],
        )


@strawberry.type
class AuthorConnection:
    page_info: LazyPageInfo
    nodes: List[Author]
    total_count: int
