from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Iterable, List, Optional, Type

from dataclasses_json import dataclass_json

from ..page import (
    LimitOffsetCursor,
    LimitOffsetPage,
    LimitOffsetPageQuery,
    SortDirection,
)

__all__ = [
    "AuthorCursor",
    "AuthorDto",
    "AuthorPage",
    "AuthorQuery",
    "AuthorSort",
    "AuthorPageSortBy",
    "CreateAuthorDto",
]


@dataclass
class AuthorDto:
    id: int
    first_name: str
    last_name: str


@dataclass
class CreateAuthorDto:
    first_name: str
    last_name: str
    id: Optional[int] = None


class AuthorPageSortBy(Enum):
    CREATED_AT = "created_at"
    FIRST_NAME = "first_name"


@dataclass_json
@dataclass(frozen=True)
class AuthorSort:
    by: AuthorPageSortBy = field(default=AuthorPageSortBy.CREATED_AT)
    direction: SortDirection = field(default=SortDirection.DESC)


@dataclass_json
@dataclass(frozen=True)
class AuthorCursor(
    LimitOffsetCursor,
    limit_ceiling=5,
    limit_default=10,
):
    sorts: List[AuthorSort] = field(default_factory=list)


@dataclass(frozen=True)
class AuthorQuery(LimitOffsetPageQuery[AuthorCursor], cursor_cls=AuthorCursor):
    sorts: List[AuthorSort] = field(default_factory=list)

    def make_cursor(self) -> AuthorCursor:
        return AuthorCursor(sorts=self.sorts)


@dataclass(frozen=True)
class AuthorPage(LimitOffsetPage[AuthorQuery, AuthorDto]):
    total_count: int

    @classmethod
    def build(
        cls: Type["AuthorPage"],
        query: AuthorQuery,
        results: Iterable[AuthorDto],
        total_count: int,
    ) -> "AuthorPage":
        nodes, page_info = cls.derive_nodes_and_page_info(query, results)
        return AuthorPage(
            page_info=page_info,
            nodes=nodes,
            total_count=total_count,
        )
