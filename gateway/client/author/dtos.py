from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Iterable, List, Optional, Type

from dataclasses_json import dataclass_json

from ..page import LimitOffsetCursor, LimitOffsetPage, LimitOffsetPageQuery, SortOrder

__all__ = [
    "AuthorCursorDto",
    "AuthorDto",
    "AuthorPageDto",
    "AuthorQueryDto",
    "AuthorSortDto",
    "AuthorSortByDto",
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


class AuthorSortByDto(Enum):
    CREATED_AT = "created_at"
    FIRST_NAME = "first_name"


@dataclass_json
@dataclass(frozen=True)
class AuthorSortDto:
    by: AuthorSortByDto = field(default=AuthorSortByDto.CREATED_AT)
    order: SortOrder = field(default=SortOrder.DESC)


@dataclass_json
@dataclass(frozen=True)
class AuthorCursorDto(
    LimitOffsetCursor,
    limit_ceiling=5,
    limit_default=10,
):
    sorts: List[AuthorSortDto] = field(default_factory=list)


@dataclass(frozen=True)
class AuthorQueryDto(LimitOffsetPageQuery[AuthorCursorDto], cursor_cls=AuthorCursorDto):
    sorts: List[AuthorSortDto] = field(default_factory=list)

    def make_cursor(self) -> AuthorCursorDto:
        return AuthorCursorDto(sorts=self.sorts)


@dataclass(frozen=True)
class AuthorPageDto(LimitOffsetPage[AuthorQueryDto, AuthorDto]):
    total_count: int

    @classmethod
    def build(
        cls: Type["AuthorPageDto"],
        query: AuthorQueryDto,
        results: Iterable[AuthorDto],
        total_count: int,
    ) -> "AuthorPageDto":
        nodes, page_info = cls.derive_nodes_and_page_info(query, results)
        return AuthorPageDto(
            page_info=page_info,
            nodes=nodes,
            total_count=total_count,
        )
