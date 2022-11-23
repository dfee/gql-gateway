from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Optional

import pytest
from dataclasses_json import dataclass_json

from gateway.client.page import (
    CursorDirection,
    CursorPreference,
    LimitOffset,
    LimitOffsetCursor,
    LimitOffsetPage,
    LimitOffsetPageInfoMetadata,
    LimitOffsetPageMetadata,
    LimitOffsetPageQuery,
    PageInfo,
    SortOrder,
)
from gateway.util.dataclass import b64_encode_dataclass


@dataclass(frozen=True)
class Foo:
    id: int


class FooSortBy(Enum):
    ID = "id"


@dataclass_json
@dataclass(frozen=True)
class FooSort:
    by: FooSortBy
    order: SortOrder


@dataclass_json
@dataclass(frozen=True)
class FooLimitOffsetCursor(LimitOffsetCursor):
    # for some reason, dataclasses_json can't decode Iterable[T], just List[T]
    sorts: List[FooSort] = field(default_factory=list)


@dataclass(frozen=True)
class FooLimitOffsetPageQuery(
    LimitOffsetPageQuery[FooLimitOffsetCursor],
    cursor_cls=FooLimitOffsetCursor,
):
    sorts: Iterable[FooSort] = field(default_factory=list)

    def make_cursor(self) -> FooLimitOffsetCursor:
        return self.cursor_cls(sorts=self.sorts)


@dataclass(frozen=True)
class FooLimitOffsetPage(LimitOffsetPage[FooLimitOffsetPageQuery, Foo]):
    pass


LimitOffsetExpectations = namedtuple("LimitOffsetExpectations", ["limit", "offset"])


@pytest.mark.parametrize(
    ("limit_offset", "expectations", "results", "metadata"),
    [
        ## Beginning
        ##   SELECT * FROM foo OFFSET 0 LIMIT 1; -- returns 1st record
        [
            LimitOffset(after=0, first=0),  # Want: []
            LimitOffsetExpectations(offset=0, limit=1),  # Req: [1]
            [],  # Res (none)
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=False,
                    start_offset=0,
                    end_offset=0,
                ),
            ),
        ],
        [
            LimitOffset(after=0, first=0),  # Want: []
            LimitOffsetExpectations(offset=0, limit=1),  # Req: [1]
            [1],  # Res
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=True,
                    start_offset=0,
                    end_offset=0,
                ),
            ),
        ],
        [
            LimitOffset(after=0, first=2),  # Want: [1..2]
            LimitOffsetExpectations(offset=0, limit=3),  # Req: [1..3]
            [],  # Res (none)
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=False,
                    start_offset=0,
                    end_offset=0,
                ),
            ),
        ],
        [
            LimitOffset(after=0, first=2),  # Want: [1..2]
            LimitOffsetExpectations(offset=0, limit=3),  # Req: [1..3]
            [1],  # Res
            LimitOffsetPageMetadata(
                nodes=[1],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=False,
                    start_offset=1,
                    end_offset=1,
                ),
            ),
        ],
        [
            LimitOffset(after=0, first=2),  # Want: [1..2]
            LimitOffsetExpectations(offset=0, limit=3),  # Req: [1..3]
            [1, 2],  # Res
            LimitOffsetPageMetadata(
                nodes=[1, 2],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=False,
                    start_offset=1,
                    end_offset=2,
                ),
            ),
        ],
        [
            LimitOffset(after=0, first=2),  # Want: [1..2]
            LimitOffsetExpectations(offset=0, limit=3),  # Req: [1..3]
            [1, 2, 3],  # Res
            LimitOffsetPageMetadata(
                nodes=[1, 2],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=True,
                    start_offset=1,
                    end_offset=2,
                ),
            ),
        ],
        ## Middle:
        ##   SELECT * FROM foo OFFSET 9 LIMIT 1; -- returns 10th record
        [
            LimitOffset(after=10, first=0),  # Want: []
            LimitOffsetExpectations(offset=9, limit=2),  # Req: [10..11]
            [],  # Res (none)
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=10,
                    end_offset=10,
                ),
            ),
        ],
        [
            LimitOffset(after=10, first=0),  # Want: []
            LimitOffsetExpectations(offset=9, limit=2),  # Req: [10..11]
            [10],  # Res (none)
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=10,
                    end_offset=10,
                ),
            ),
        ],
        [
            LimitOffset(after=10, first=2),  # Want: [11..12]
            LimitOffsetExpectations(offset=9, limit=4),  # Req: [10..13]
            [],  # Res (none)
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=10,
                    end_offset=10,
                ),
            ),
        ],
        [
            LimitOffset(after=10, first=2),  # Want: [11..12]
            LimitOffsetExpectations(offset=9, limit=4),  # Req: [10..13]
            [10],  # Res
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=11,
                    end_offset=11,
                ),
            ),
        ],
        [
            LimitOffset(after=10, first=2),  # Want: [11..12]
            LimitOffsetExpectations(offset=9, limit=4),  # Req: [10..13]
            [10, 11],  # Res
            LimitOffsetPageMetadata(
                nodes=[11],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=11,
                    end_offset=11,
                ),
            ),
        ],
        [
            LimitOffset(after=10, first=2),  # Want: [11..12]
            LimitOffsetExpectations(offset=9, limit=4),  # Req: [10..13]
            [10, 11, 12],  # Res
            LimitOffsetPageMetadata(
                nodes=[11, 12],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=11,
                    end_offset=12,
                ),
            ),
        ],
        [
            LimitOffset(after=10, first=2),  # Want: [11..12]
            LimitOffsetExpectations(offset=9, limit=4),  # Req: [10..13]
            [10, 11, 12, 13],  # Res
            LimitOffsetPageMetadata(
                nodes=[11, 12],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=True,
                    start_offset=11,
                    end_offset=12,
                ),
            ),
        ],
    ],
)
def test_limit_offset(
    results: Iterable[int],
    limit_offset: LimitOffset,
    expectations: LimitOffsetExpectations,
    metadata: LimitOffsetPageInfoMetadata,
) -> None:
    assert limit_offset.limit == expectations.limit
    assert limit_offset.offset == expectations.offset
    assert limit_offset.to_page_metadata(results) == metadata


@pytest.mark.parametrize(
    ("reverse", "forward"),
    [
        [
            LimitOffset.reverse(before=0, last=2),  # Want: []
            LimitOffset(after=0, first=0),
        ],
        [
            LimitOffset.reverse(before=1, last=2),  # Want []
            LimitOffset(after=0, first=0),
        ],
        [
            LimitOffset.reverse(before=2, last=2),  # Want: [1]
            LimitOffset(after=0, first=1),
        ],
        [
            LimitOffset.reverse(before=3, last=2),  # Want: [1..2]
            LimitOffset(after=0, first=2),
        ],
        [
            LimitOffset.reverse(before=4, last=2),  # Want: [2..3]
            LimitOffset(after=1, first=2),
        ],
    ],
)
def test_limit_offset_reverse(
    reverse: LimitOffset,
    forward: LimitOffset,
) -> None:
    assert reverse == forward


@pytest.mark.parametrize(
    ("offset", "limit", "direction", "limit_offset"),
    [
        [
            0,
            None,
            CursorDirection.AFTER,
            LimitOffset(after=0, first=FooLimitOffsetCursor.limit_default),
        ],
        [
            0,
            3,
            CursorDirection.AFTER,
            LimitOffset(after=0, first=3),
        ],
        [
            5,
            None,
            CursorDirection.AFTER,
            LimitOffset(after=5, first=FooLimitOffsetCursor.limit_default),
        ],
        [
            0,
            999,  # clamped
            CursorDirection.AFTER,
            LimitOffset(after=0, first=FooLimitOffsetCursor.limit_ceiling),
        ],
        [
            15,
            None,
            CursorDirection.BEFORE,
            LimitOffset(after=4, first=FooLimitOffsetCursor.limit_default),
        ],
        [
            15,
            3,
            CursorDirection.BEFORE,
            LimitOffset(after=11, first=3),
        ],
    ],
)
def test_to_limit_offset(
    offset: int,
    limit: int,
    direction: CursorDirection,
    limit_offset: LimitOffset,
) -> None:
    ins = FooLimitOffsetCursor(offset=offset)
    assert ins.make_limit_offset(direction=direction, limit=limit) == limit_offset


def test_limit_offset_cursor__replace_offset():
    cursor = FooLimitOffsetCursor(
        offset=0,
        sorts=[FooSort(by=FooSortBy.ID, order=SortOrder.ASC)],
    )
    assert cursor.replace_offset(5) == FooLimitOffsetCursor(
        offset=5,
        sorts=cursor.sorts,
    )


def test_limit_offset_cursor__codec():
    cursor = FooLimitOffsetCursor(
        offset=0,
        sorts=[FooSort(by=FooSortBy.ID, order=SortOrder.ASC)],
    )
    assert FooLimitOffsetCursor.decode(cursor.encode()) == cursor


@pytest.mark.parametrize(
    ("after", "before", "expected_cursor_preference", "get_expected_cursor"),
    [
        [
            FooLimitOffsetCursor(offset=0),
            FooLimitOffsetCursor(offset=10),
            CursorPreference.AFTER,
            lambda query: query.after_cursor,
        ],
        [
            None,
            FooLimitOffsetCursor(offset=10),
            CursorPreference.BEFORE,
            lambda query: query.before_cursor,
        ],
        [
            None,
            None,
            CursorPreference.DEFAULT,
            lambda query: query.make_cursor(),
        ],
    ],
)
def test_page_query_canonical_cursor(
    after: Optional[FooLimitOffsetCursor],
    before: Optional[FooLimitOffsetCursor],
    expected_cursor_preference: CursorPreference,
    get_expected_cursor,
):
    query = FooLimitOffsetPageQuery(
        after=(after.encode() if after else None),
        before=(before.encode() if before else None),
    )
    assert query.cursor_preference == expected_cursor_preference
    assert query.preferred_cursor == get_expected_cursor(query)


@pytest.mark.parametrize(
    ("query", "expected_limit_offset"),
    [
        [
            FooLimitOffsetPageQuery(
                after=FooLimitOffsetCursor(offset=10).encode(),
                first=3,
            ),
            LimitOffset(after=10, first=3),
        ],
        [
            FooLimitOffsetPageQuery(
                before=FooLimitOffsetCursor(offset=10).encode(),
                last=3,
            ),
            LimitOffset(after=6, first=3),
        ],
        [
            FooLimitOffsetPageQuery(
                first=3,
            ),
            LimitOffset(after=0, first=3),
        ],
    ],
)
def test_limit_offset_page_query__make_limit_offset(
    query: FooLimitOffsetPageQuery,
    expected_limit_offset: LimitOffset,
):
    assert query.limit_offset == expected_limit_offset


def test_limit_offset_page_metadata__page_info_from_template_cursor():
    metadata = LimitOffsetPageMetadata(
        nodes=[0, 1],
        page_info_metadata=LimitOffsetPageInfoMetadata(
            end_offset=5,
            start_offset=10,
            has_next_page=True,
            has_previous_page=True,
        ),
    )

    template_cursor = FooLimitOffsetCursor(
        offset=4,
        sorts=[FooSort(by=FooSortBy.ID, order=SortOrder.ASC)],
    )

    assert metadata.page_info_from_template_cursor(template_cursor) == PageInfo(
        has_next_page=metadata.page_info_metadata.has_next_page,
        has_previous_page=metadata.page_info_metadata.has_previous_page,
        start_cursor=FooLimitOffsetCursor(
            offset=metadata.page_info_metadata.start_offset,
            sorts=template_cursor.sorts,
        ).encode(),
        end_cursor=FooLimitOffsetCursor(
            offset=metadata.page_info_metadata.end_offset,
            sorts=template_cursor.sorts,
        ).encode(),
    )


_SORTS = [FooSort(by=FooSortBy.ID, order=SortOrder.ASC)]


@pytest.mark.parametrize(
    ("query", "results", "expected_nodes", "expected_page_info"),
    [
        [
            FooLimitOffsetPageQuery(  # Want: [Foo(1)..Foo(2)]
                first=2,
                sorts=_SORTS,
            ),
            [Foo(id) for id in range(1, 4)],  # Have: [Foo(1)..Foo(3)]
            [Foo(id) for id in range(1, 3)],  # Get: [Foo(1)..Foo(2)]
            PageInfo(
                has_previous_page=False,
                has_next_page=True,
                start_cursor=FooLimitOffsetCursor(
                    offset=1,
                    sorts=_SORTS,
                ).encode(),
                end_cursor=FooLimitOffsetCursor(
                    offset=2,
                    sorts=_SORTS,
                ).encode(),
            ),
        ],
        [
            FooLimitOffsetPageQuery(  # Want: [Foo(3)..Foo(4)]
                after=FooLimitOffsetCursor(
                    offset=2,
                    sorts=_SORTS,
                ).encode(),
                first=2,
            ),
            [Foo(id) for id in range(2, 5)],  # Have: [Foo(2)..Foo(4)]
            [Foo(id) for id in range(3, 5)],  # Get: [Foo(3)..Foo(4)]
            PageInfo(
                has_previous_page=True,
                has_next_page=False,
                start_cursor=FooLimitOffsetCursor(
                    offset=3,
                    sorts=_SORTS,
                ).encode(),
                end_cursor=FooLimitOffsetCursor(
                    offset=4,
                    sorts=_SORTS,
                ).encode(),
            ),
        ],
    ],
)
def test_limit_offset_page__derive_nodes_and_page_info(
    query: FooLimitOffsetPageQuery,
    results: Iterable[Foo],
    expected_nodes: Iterable[Foo],
    expected_page_info: PageInfo,
) -> None:
    nodes, page_info = FooLimitOffsetPage.derive_nodes_and_page_info(
        query,
        results,
    )
    assert nodes == expected_nodes
    assert page_info == expected_page_info
