from collections import namedtuple
from dataclasses import dataclass, field, replace
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
    has_even_id: Optional[bool] = field(default=None)


@dataclass(frozen=True)
class FooLimitOffsetPageQuery(
    LimitOffsetPageQuery[FooLimitOffsetCursor],
    cursor_cls=FooLimitOffsetCursor,
):
    sorts: Iterable[FooSort] = field(default_factory=list)
    has_even_id: Optional[bool] = field(default=None)

    def make_cursor(self) -> FooLimitOffsetCursor:
        return self.cursor_cls(
            sorts=self.sorts,
            has_even_id=self.has_even_id,
        )


class FooLimitOffsetPage(LimitOffsetPage[FooLimitOffsetPageQuery, Foo]):
    pass


LimitOffsetExpectations = namedtuple("LimitOffsetExpectations", ["limit", "offset"])


@pytest.mark.parametrize(
    ("node_count", "limit_offset", "expectations", "metadata"),
    [
        ## Beginning
        [  # Want: [0, 1] -> Req: [0, 1, 2] -> Res: [] -> Get: []
            0,
            LimitOffset(after=0, first=2),
            LimitOffsetExpectations(offset=0, limit=3),
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
        [  # Want: [0, 1] -> Req: [0, 1, 2] -> Res: [0] -> Get: [0]
            1,
            LimitOffset(after=0, first=2),
            LimitOffsetExpectations(offset=0, limit=3),
            LimitOffsetPageMetadata(
                nodes=[0],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=False,
                    start_offset=1,
                    end_offset=1,
                ),
            ),
        ],
        [  # Want: [0, 1] -> Req: [0, 1, 2] -> Res: [0, 1] -> Get: [0, 1]
            2,
            LimitOffset(after=0, first=2),
            LimitOffsetExpectations(offset=0, limit=3),
            LimitOffsetPageMetadata(
                nodes=[0, 1],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=False,
                    start_offset=1,
                    end_offset=2,
                ),
            ),
        ],
        [  # Want: [0, 1] -> Req: [0, 1, 2] -> Res: [0, 1, 2] -> Get: [0, 1]
            3,
            LimitOffset(after=0, first=2),
            LimitOffsetExpectations(offset=0, limit=3),
            LimitOffsetPageMetadata(
                nodes=[0, 1],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=False,
                    has_next_page=True,
                    start_offset=1,
                    end_offset=2,
                ),
            ),
        ],
        ## Middle
        [  # Want: [1, 2] -> Req: [0, 1, 2, 3] -> Res: [] -> Get: []
            0,
            LimitOffset(after=1, first=2),
            LimitOffsetExpectations(offset=0, limit=4),
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
        [  # Want: [1, 2] -> Req: [0, 1, 2, 3] -> Res: [0] -> Get: []
            1,
            LimitOffset(after=1, first=2),
            LimitOffsetExpectations(offset=0, limit=4),
            LimitOffsetPageMetadata(
                nodes=[],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=1,
                    end_offset=1,
                ),
            ),
        ],
        [  # Want: [1, 2] -> Req: [0, 1, 2, 3] -> Res: [0, 1] -> Get: [1]
            2,
            LimitOffset(after=1, first=2),
            LimitOffsetExpectations(offset=0, limit=4),
            LimitOffsetPageMetadata(
                nodes=[1],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=2,
                    end_offset=2,
                ),
            ),
        ],
        [  # Want: [1, 2] -> Req: [0, 1, 2, 3] -> Res: [0, 1, 2] -> Get: [1, 2]
            3,
            LimitOffset(after=1, first=2),
            LimitOffsetExpectations(offset=0, limit=4),
            LimitOffsetPageMetadata(
                nodes=[1, 2],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=False,
                    start_offset=2,
                    end_offset=3,
                ),
            ),
        ],
        [  # Want: [1, 2] -> Req: [0, 1, 2, 3] -> Res: [0, 1, 2, 3] -> Get: [1, 2]
            4,
            LimitOffset(after=1, first=2),
            LimitOffsetExpectations(offset=0, limit=4),
            LimitOffsetPageMetadata(
                nodes=[1, 2],
                page_info_metadata=LimitOffsetPageInfoMetadata(
                    has_previous_page=True,
                    has_next_page=True,
                    start_offset=2,
                    end_offset=3,
                ),
            ),
        ],
    ],
)
def test_limit_offset(
    node_count: int,
    limit_offset: LimitOffset,
    expectations: LimitOffsetExpectations,
    metadata: LimitOffsetPageInfoMetadata,
) -> None:
    assert limit_offset.limit == expectations.limit
    assert limit_offset.offset == expectations.offset
    nodes = list(range(node_count))

    assert limit_offset.to_page_metadata(nodes) == metadata


@pytest.mark.parametrize(
    ("reverse", "forward"),
    [
        [
            LimitOffset.reverse(before=0, last=2),
            LimitOffset(after=0, first=0),
        ],
        [
            LimitOffset.reverse(before=1, last=2),
            LimitOffset(after=0, first=1),
        ],
        [
            LimitOffset.reverse(before=2, last=2),
            LimitOffset(after=0, first=2),
        ],
        [
            LimitOffset.reverse(before=3, last=2),
            LimitOffset(after=1, first=2),
        ],
        [
            LimitOffset.reverse(before=4, last=2),
            LimitOffset(after=2, first=2),
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
            LimitOffset(after=5, first=FooLimitOffsetCursor.limit_default),
        ],
        [
            15,
            3,
            CursorDirection.BEFORE,
            LimitOffset(after=12, first=3),
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
        has_even_id=True,
    )
    assert cursor.replace_offset(5) == FooLimitOffsetCursor(
        offset=5,
        sorts=cursor.sorts,
        has_even_id=cursor.has_even_id,
    )


def test_limit_offset_cursor__codec():
    cursor = FooLimitOffsetCursor(
        offset=0,
        sorts=[FooSort(by=FooSortBy.ID, order=SortOrder.ASC)],
        has_even_id=True,
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
            LimitOffset(after=7, first=3),
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
        has_even_id=True,
    )

    assert metadata.page_info_from_template_cursor(template_cursor) == PageInfo(
        has_next_page=metadata.page_info_metadata.has_next_page,
        has_previous_page=metadata.page_info_metadata.has_previous_page,
        start_cursor=FooLimitOffsetCursor(
            offset=metadata.page_info_metadata.start_offset,
            sorts=template_cursor.sorts,
            has_even_id=template_cursor.has_even_id,
        ).encode(),
        end_cursor=FooLimitOffsetCursor(
            offset=metadata.page_info_metadata.end_offset,
            sorts=template_cursor.sorts,
            has_even_id=template_cursor.has_even_id,
        ).encode(),
    )


def test_limit_offset_page__derive_nodes_and_page_info():
    query = FooLimitOffsetPageQuery(
        first=5,
        has_even_id=True,
        sorts=[FooSort(by=FooSortBy.ID, order=SortOrder.ASC)],
    )
    results = [Foo(id) for id in range(6)]

    nodes, page_info = FooLimitOffsetPage.derive_nodes_and_page_info(
        query,
        results,
    )

    assert nodes == results[0:5]
    assert page_info == PageInfo(
        has_previous_page=False,
        has_next_page=True,
        start_cursor=query.preferred_cursor.replace_offset(1).encode(),
        end_cursor=query.preferred_cursor.replace_offset(5).encode(),
    )
