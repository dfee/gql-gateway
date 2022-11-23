from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from enum import Enum
from functools import cached_property
from typing import Any, ClassVar, Generic, Iterable, Optional, Tuple, Type, TypeVar

from gateway.util.dataclass import b64_decode_dataclass, b64_encode_dataclass

__all__ = [
    "CursorDirection",
    "CursorPreference",
    "LimitOffset",
    "LimitOffsetCursor",
    "LimitOffsetPage",
    "LimitOffsetPageInfoMetadata",
    "LimitOffsetPageMetadata",
    "LimitOffsetPageQuery",
    "Page",
    "PageInfo",
    "PageQuery",
    "SortOrder",
]


T = TypeVar("T")


class CursorDirection(Enum):
    AFTER = "after"
    BEFORE = "before"


class CursorPreference(Enum):
    AFTER = "after"
    BEFORE = "before"
    DEFAULT = "default"


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


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


@dataclass(frozen=True)
class PageQuery(ABC, Generic[T]):
    cursor_cls: ClassVar[Type[T]]
    before: Optional[str] = field(default=None)
    after: Optional[str] = field(default=None)
    first: Optional[int] = field(default=None)
    last: Optional[int] = field(default=None)

    def __init_subclass__(cls, *, cursor_cls: Type[T], **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.cursor_cls = cursor_cls

    @cached_property
    def cursor_preference(self) -> CursorPreference:
        if self.after:
            return CursorPreference.AFTER
        if self.before:
            return CursorPreference.BEFORE
        return CursorPreference.DEFAULT

    @cached_property
    def after_cursor(self) -> Optional[T]:
        return self.cursor_cls.decode(self.after) if self.after else None

    @cached_property
    def before_cursor(self) -> Optional[T]:
        return self.cursor_cls.decode(self.before) if self.before else None

    @abstractmethod
    def make_cursor(self) -> T:
        """
        Make a cursor for slicing based on properties of this PageQuery subtype.
        Generally includes all properties except: after, before, first, & last.
        """
        pass

    @cached_property
    def preferred_cursor(self) -> T:
        """
        The cursor for slicing the query, by preference: after, before, default.
        """
        if self.cursor_preference is CursorPreference.AFTER:
            return self.after_cursor
        if self.cursor_preference is CursorPreference.BEFORE:
            return self.before_cursor
        if self.cursor_preference is CursorPreference.DEFAULT:
            return self.make_cursor()


@dataclass(frozen=True)
class LimitOffset:
    after: int
    first: int

    @property
    def limit(self):
        if self.after:
            return self.first + 2
        return self.first + 1

    @property
    def offset(self):
        if self.after:
            return self.after - 1
        return self.after

    def to_page_metadata(
        self,
        results: Iterable[Any],
    ) -> "LimitOffsetPageMetadata":
        results_count = len(results)
        if self.after > 0:
            start_offset = (
                self.after if not results or not self.first else self.after + 1
            )
            end_offset = min(
                (
                    self.after
                    if results_count == 0
                    else self.after + 1
                    if results_count <= 2
                    else self.after + results_count
                ),
                self.after + self.first,
            )
            return LimitOffsetPageMetadata(
                nodes=results[1 : self.limit - 1],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=results_count == self.limit,
                    start_offset=start_offset,
                    end_offset=end_offset,
                ),
            )

        return LimitOffsetPageMetadata(
            nodes=results[: self.limit - 1],
            page_info_metadata=LimitOffsetPageInfoMetadata(
                has_previous_page=False,
                has_next_page=results_count == self.limit,
                start_offset=(0 if not results or not self.first else 1),
                end_offset=max(0, min(results_count, self.first)),
            ),
        )

    @classmethod
    def reverse(cls: "LimitOffset", before: int, last: int) -> "LimitOffset":
        if before - last > 0:
            return cls(after=before - last - 1, first=last)
        return cls(after=0, first=max(0, before - 1))


@dataclass(frozen=True)
class LimitOffsetCursor(ABC):
    offset: int = field(default=0)
    limit_ceiling: ClassVar[int]
    limit_default: ClassVar[int]

    def __init_subclass__(cls, limit_default=10, limit_ceiling=100, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.limit_default = limit_default
        cls.limit_ceiling = limit_ceiling

    def make_limit_offset(
        self,
        direction: CursorDirection,
        limit: Optional[int] = None,
    ) -> LimitOffset:
        _limit = self._clamp_limit(limit)
        if direction is CursorDirection.AFTER:
            return LimitOffset(after=self.offset, first=_limit)
        return LimitOffset.reverse(before=self.offset, last=_limit)

    def replace_offset(self, offset: int):
        return replace(self, offset=offset)

    def encode(self):
        return b64_encode_dataclass(self)

    @classmethod
    def decode(cls: Type[T], value: str) -> T:
        return b64_decode_dataclass(cls, value)

    @classmethod
    def _clamp_limit(cls, value: Optional[int]) -> int:
        return max(
            0,
            min(
                cls.limit_ceiling,
                next(v for v in [value, cls.limit_default] if v is not None),
            ),
        )


LOC = TypeVar("LOC", bound=LimitOffsetCursor)


@dataclass(frozen=True)
class LimitOffsetPageInfoMetadata:
    end_offset: int
    has_next_page: bool
    has_previous_page: bool
    start_offset: int


@dataclass
class LimitOffsetPageMetadata(Generic[T]):
    nodes: Iterable[T]
    page_info_metadata: LimitOffsetPageInfoMetadata

    def page_info_from_template_cursor(self, template_cursor: LOC) -> PageInfo:
        md = self.page_info_metadata
        return PageInfo(
            has_next_page=md.has_next_page,
            has_previous_page=md.has_previous_page,
            start_cursor=template_cursor.replace_offset(md.start_offset).encode(),
            end_cursor=template_cursor.replace_offset(md.end_offset).encode(),
        )


@dataclass(frozen=True)
class LimitOffsetPageQuery(PageQuery[LOC], Generic[LOC], cursor_cls=...):
    @cached_property
    def limit_offset(self) -> LimitOffset:
        if self.cursor_preference is CursorPreference.BEFORE:
            return self.preferred_cursor.make_limit_offset(
                direction=CursorDirection.BEFORE,
                limit=self.last,
            )
        return self.preferred_cursor.make_limit_offset(
            direction=CursorDirection.AFTER,
            limit=self.first,
        )


LOC_Q = TypeVar("LOC_Q", bound=LimitOffsetPageQuery)


@dataclass(frozen=True)
class LimitOffsetPage(Page[T], Generic[LOC_Q, T]):
    @classmethod
    def derive_nodes_and_page_info(
        cls,
        query: LOC_Q,
        results: Iterable[T],
    ) -> Tuple[Iterable[T], PageInfo]:
        page_metadata = query.limit_offset.to_page_metadata(results)
        page_info = page_metadata.page_info_from_template_cursor(query.preferred_cursor)
        return page_metadata.nodes, page_info
