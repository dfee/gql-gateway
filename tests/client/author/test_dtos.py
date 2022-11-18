import pytest

from gateway.client.author import (
    AuthorCursorDto,
    AuthorDto,
    AuthorQueryDto,
    AuthorSortDto,
)
from tests.util.dataclass import assert_b64_codec


def author_fixture(id: int) -> AuthorDto:
    return AuthorDto(id, first_name=f"first_{id}", last_name=f"last_{id}")


class TestAuthorSort:
    @pytest.mark.parametrize("sort", [AuthorSortDto()])
    def test_codec(self, sort) -> None:
        assert_b64_codec(AuthorSortDto, sort)


@pytest.mark.parametrize("cursor", [AuthorCursorDto()])
def test_author_cursor_codec(cursor: AuthorCursorDto) -> None:
    assert_b64_codec(AuthorCursorDto, cursor)


@pytest.mark.parametrize(
    ("query", "cursor"),
    [
        [AuthorQueryDto(), AuthorCursorDto()],
        [
            AuthorQueryDto(sorts=[AuthorSortDto()]),
            AuthorCursorDto(sorts=[AuthorSortDto()]),
        ],
    ],
)
def test_author_query_make_cursor(
    query: AuthorQueryDto, cursor: AuthorCursorDto
) -> None:
    assert query.make_cursor() == cursor
