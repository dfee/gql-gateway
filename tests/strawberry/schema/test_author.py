import pytest

from gateway.strawberry.schema import (
    AuthorQueryInput,
    AuthorSortBy,
    AuthorSortInput,
    SortOrder,
)


@pytest.mark.parametrize(("member",), [[m] for m in AuthorSortBy])
def test_author_sort_by_codec(member: AuthorSortBy) -> None:
    assert AuthorSortBy.from_dto(member.to_dto()) == member


def test_author_sort_input_codec():
    ins = AuthorSortInput(by=AuthorSortBy.CREATED_AT, order=SortOrder.ASC)
    assert AuthorSortInput.from_dto(ins.to_dto()) == ins


def test_author_query_input():
    ins = AuthorQueryInput(
        after="after",
        before="before",
        first=5,
        last=10,
        sorts=[AuthorSortInput(by=AuthorSortBy.CREATED_AT, order=SortOrder.ASC)],
    )
    assert AuthorQueryInput.from_dto(ins.to_dto()) == ins
