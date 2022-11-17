from dataclasses import replace
from typing import Optional

import pytest

from gateway.client.author import AuthorCursor, AuthorDto, AuthorQuery, AuthorSort
from gateway.client.page import (
    AfterLimitOffset,
    BeforeLimitOffset,
    CursorDirection,
    PageInfo,
)
from gateway.util.dataclass import b64_encode_dataclass
from tests.util.dataclass import assert_b64_codec


def author_fixture(id: int) -> AuthorDto:
    return AuthorDto(id, first_name=f"first_{id}", last_name=f"last_{id}")


AUTHOR_SORT = AuthorSort()


class TestAuthorSort:
    @pytest.mark.parametrize("sort", [AUTHOR_SORT])
    def test_codec(self, sort) -> None:
        assert_b64_codec(AuthorSort, sort)


AUTHOR_CURSOR = AuthorCursor.with_defaults()


class TestAuthorPageCursor:
    @pytest.mark.parametrize("cursor", [AUTHOR_CURSOR])
    def test_codec(self, cursor: AuthorCursor) -> None:
        assert_b64_codec(AuthorCursor, cursor)

    @pytest.mark.parametrize(
        "direction,expected",
        [
            [
                CursorDirection.AFTER,
                AfterLimitOffset(_after=20, _first=10),
            ],
            [
                CursorDirection.BEFORE,
                BeforeLimitOffset(_before=20, _last=10),
            ],
        ],
    )
    def test_limit_offset(self, direction, expected) -> None:
        cursor = AuthorCursor(limit=10, offset=20, sorts=[AuthorSort()])
        assert cursor.to_limit_offset(direction) == expected


class TestAuthorQuery:
    cursor = AuthorCursor.with_defaults(limit=5, offset=10, sorts=[AUTHOR_SORT])
    cursor_s = b64_encode_dataclass(cursor)

    @pytest.mark.parametrize("limit", [3, None])
    def test_cursor__after(self, limit: Optional[int]) -> None:
        aq = AuthorQuery(after=self.cursor_s, first=limit)
        assert (
            aq.cursor == self.cursor
            if limit is None
            else replace(self.cursor, limit=limit)
        )

    @pytest.mark.parametrize("limit", [3, None])
    def test_cursor__before(self, limit: Optional[int]) -> None:
        aq = AuthorQuery(before=self.cursor_s, last=limit)
        assert (
            aq.cursor == self.cursor
            if limit is None
            else replace(self.cursor, limit=limit)
        )

    @pytest.mark.parametrize("limit", [3, None])
    def test_cursor__default(self, limit: Optional[int]) -> None:
        aq = AuthorQuery(first=limit)
        assert aq.cursor == AuthorCursor.with_defaults(limit=limit)

    def test_to_page_info_empty(self):
        aq = AuthorQuery()
        page_info = aq.to_page_info([])
        assert page_info == PageInfo(
            has_next_page=False,
            has_previous_page=False,
            start_cursor=None,
            end_cursor=None,
        )

    def test_to_page_info_full(self):
        aq = AuthorQuery(first=3, after=self.cursor_s)
        offset = aq.limit_offset.offset
        assert offset == 10, "sanity"
        limit = aq.limit_offset.limit
        assert limit == 3 + 1, "sanity"
        nodes = [author_fixture(id) for id in range(offset, offset + limit)]

        page_info = aq.to_page_info(nodes)
        assert page_info.has_next_page
        assert page_info.has_previous_page
        assert AuthorCursor.decode(page_info.start_cursor) == AuthorCursor(
            limit=3,  # from provided `first`
            offset=11,  # offset of 10, take the next one, thus the 11th record
            sorts=self.cursor.sorts,
        )
        assert AuthorCursor.decode(page_info.end_cursor) == AuthorCursor(
            limit=3,  # (also) from provided `first`
            offset=13,  # offset of 10, take the third one, thus the 13th record
            sorts=self.cursor.sorts,
        )
