from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Callable, ClassVar, Generic, Iterable, Optional, Type, TypeVar

from gateway.util.dataclass import b64_decode_dataclass

__all__ = [
    "AfterLimitOffset",
    "BeforeLimitOffset",
    "CursorDirection",
    "LimitOffset",
    "LimitOffsetCursor",
    "LimitOffsetPageInfoMetadata",
    "Page",
    "PageInfo",
    "PageQuery",
    "SortDirection",
]

T = TypeVar("T")


@dataclass(frozen=True)
class PageQuery(ABC):
    before: Optional[str] = field(default=None)
    after: Optional[str] = field(default=None)
    first: Optional[int] = field(default=None)
    last: Optional[int] = field(default=None)

    @abstractproperty
    def cursor(self) -> T:
        pass


@dataclass(frozen=True)
class PageInfo:
    has_previous_page: bool
    has_next_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]


@dataclass(frozen=True)
class Page(Generic[T]):
    page_info: PageInfo
    nodes: Iterable[T]


class CursorDirection(Enum):
    AFTER = "after"
    BEFORE = "before"


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True)
class LimitOffsetPageInfoMetadata:
    end_offset: Optional[int]
    start_offset: Optional[int]
    first: Optional[int] = field(default=None)
    last: Optional[int] = field(default=None)

    @property
    def has_next_page(self):
        return self.end_offset is not None

    @property
    def has_previous_page(self):
        return self.start_offset is not None


@dataclass(frozen=True)
class LimitOffset(ABC):
    @abstractproperty
    def limit(self):
        pass

    @abstractproperty
    def offset(self):
        pass

    @abstractmethod
    def to_page_info_metadata(
        self,
        results: Iterable[Any],
    ) -> LimitOffsetPageInfoMetadata:
        pass


@dataclass(frozen=True)
class AfterLimitOffset(LimitOffset):
    _after: int
    _first: int

    @property
    def limit(self):
        return self._first + 1

    @property
    def offset(self):
        return self._after

    def to_page_info_metadata(
        self,
        results: Iterable[Any],
    ) -> LimitOffsetPageInfoMetadata:
        has_sentinel = len(results) == self.limit
        after = self._after + self._first if has_sentinel else None
        first = self._first if has_sentinel else None
        before = self._after + 1 if self._after > 0 else None
        last = min(self._first, self._after) if self._after > 0 else None

        return LimitOffsetPageInfoMetadata(
            end_offset=after,
            first=first,
            start_offset=before,
            last=last,
        )


@dataclass(frozen=True)
class BeforeLimitOffset(LimitOffset):
    _before: int
    _last: int

    @property
    def limit(self):
        return self._before if self._before - self._last < 0 else self._last

    @property
    def offset(self):
        return max(self._before - self._last - 1, 0)

    def to_page_info_metadata(
        self,
        results: Iterable[Any],
    ) -> LimitOffsetPageInfoMetadata:
        has_sentinel = len(results) == self.limit
        has_head = self._before - self._last == 0
        after = max(self._before - 1, 0)
        first = self._last
        before = self._before - self._last if (has_sentinel and not has_head) else None
        last = (self._last if self._last <= before else before) if before else None

        return LimitOffsetPageInfoMetadata(
            end_offset=after,
            first=first,
            start_offset=before,
            last=last,
        )


@dataclass(frozen=True)
class LimitOffsetCursor(ABC):
    limit: int
    offset: int
    limiter: ClassVar[Callable[..., int]]

    def to_limit_offset(
        self,
        direction: CursorDirection,
    ) -> LimitOffset:
        return (
            AfterLimitOffset(
                _after=self.offset,
                _first=self.limit,
            )
            if direction is CursorDirection.AFTER
            else BeforeLimitOffset(
                _before=self.offset,
                _last=self.limit,
            )
        )

    @classmethod
    def decode(
        cls: Type[T],
        value: str,
        limit: int = None,
    ) -> T:
        cursor: "LimitOffsetCursor" = b64_decode_dataclass(cls, value)
        return replace(cursor, limit=cls.limiter(limit, cursor.limit))

    @classmethod
    def with_defaults(cls: Type[T], **kwargs) -> T:
        return cls(**{"limit": 100, "offset": 0, **kwargs})
