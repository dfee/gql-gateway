import pytest

from gateway.author.dtos import AuthorCursorDto


class TestAuthorCursor:
    @pytest.fixture
    def min(self):
        return AuthorCursorDto(offset=10)

    def test_identity(self, min: AuthorCursorDto) -> None:
        assert AuthorCursorDto.deserialize(min.serialize()) == min
