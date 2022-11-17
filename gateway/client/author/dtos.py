from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import Iterable, List, Optional, Type

from dataclasses_json import dataclass_json

from gateway.util.cursor import make_limiter
from gateway.util.dataclass import b64_encode_dataclass

from ..page import (
    CursorDirection,
    LimitOffsetCursor,
    Page,
    PageInfo,
    PageQuery,
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


DEFAULT_AUTHOR_LIMIT = 10
MAX_AUTHOR_LIMIT = 100


@dataclass_json
@dataclass(frozen=True)
class AuthorCursor(LimitOffsetCursor):
    sorts: List[AuthorSort] = field(default_factory=list)
    limiter = make_limiter(DEFAULT_AUTHOR_LIMIT, MAX_AUTHOR_LIMIT)

    @classmethod
    def with_defaults(cls: Type["AuthorCursor"], **kwargs) -> "AuthorCursor":
        limit = kwargs.pop("limit", DEFAULT_AUTHOR_LIMIT)
        return super().with_defaults(limit=cls.limiter(limit), **kwargs)


@dataclass(frozen=True)
class AuthorQuery(PageQuery):
    sorts: List[AuthorSort] = field(default_factory=list)

    @cached_property
    def cursor(self):
        if self.after:
            return AuthorCursor.decode(self.after, limit=self.first)
        if self.before:
            return AuthorCursor.decode(self.before, limit=self.last)
        return AuthorCursor.with_defaults(limit=self.first, sorts=self.sorts)

    @cached_property
    def limit_offset(self):
        return (
            self.cursor.to_limit_offset(CursorDirection.BEFORE)
            if self.before
            else self.cursor.to_limit_offset(CursorDirection.AFTER)
        )

    def to_page_info(
        self,
        nodes: Iterable[AuthorDto],
    ) -> PageInfo:
        metadata = self.limit_offset.to_page_info_metadata(nodes)
        return PageInfo(
            has_next_page=metadata.has_next_page,
            has_previous_page=metadata.has_previous_page,
            start_cursor=(
                b64_encode_dataclass(
                    AuthorCursor(
                        limit=AuthorCursor.limiter(metadata.last),
                        offset=metadata.start_offset,
                        sorts=self.cursor.sorts,
                    )
                )
                # todo: bug, should return regardless of next page
                if metadata.has_previous_page
                else None
            ),
            end_cursor=(
                b64_encode_dataclass(
                    AuthorCursor(
                        limit=AuthorCursor.limiter(metadata.first),
                        offset=metadata.end_offset,
                        sorts=self.cursor.sorts,
                    )
                )
                # todo: bug, should return regardless of next page
                if metadata.has_next_page
                else None
            ),
        )


@dataclass(frozen=True)
class AuthorPage(Page[AuthorDto]):
    @classmethod
    def from_query_and_nodes(
        cls: Type["AuthorPage"],
        query: AuthorQuery,
        nodes: Iterable[AuthorDto],
    ) -> "AuthorPage":
        page_info = query.to_page_info(nodes)
        # todo: extract this logic
        mut_nodes = nodes[::]
        if query.before and page_info.has_previous_page:
            mut_nodes.pop(0)
        elif page_info.has_next_page:
            mut_nodes.pop()
        return AuthorPage(
            page_info=page_info,
            nodes=mut_nodes,
        )
