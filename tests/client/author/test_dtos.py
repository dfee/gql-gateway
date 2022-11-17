import pytest

from gateway.client.author import AuthorCursor, AuthorDto, AuthorQuery, AuthorSort
from tests.util.dataclass import assert_b64_codec


def author_fixture(id: int) -> AuthorDto:
    return AuthorDto(id, first_name=f"first_{id}", last_name=f"last_{id}")


class TestAuthorSort:
    @pytest.mark.parametrize("sort", [AuthorSort()])
    def test_codec(self, sort) -> None:
        assert_b64_codec(AuthorSort, sort)


@pytest.mark.parametrize("cursor", [AuthorCursor()])
def test_author_cursor_codec(cursor: AuthorCursor) -> None:
    assert_b64_codec(AuthorCursor, cursor)


@pytest.mark.parametrize(
    ("query", "cursor"),
    [
        [AuthorQuery(), AuthorCursor()],
        [AuthorQuery(sorts=[AuthorSort()]), AuthorCursor(sorts=[AuthorSort()])],
    ],
)
def test_author_query_make_cursor(query: AuthorQuery, cursor: AuthorCursor) -> None:
    assert query.make_cursor() == cursor
