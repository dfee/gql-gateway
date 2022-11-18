import pytest

from gateway.graphene.schema import AuthorSortBy, AuthorSortInput, SortOrder


@pytest.mark.parametrize(("member",), [[m] for m in AuthorSortBy])
def test_author_sort_by_codec(member: AuthorSortBy) -> None:
    assert AuthorSortBy.from_dto(member.to_dto()) == member


def test_author_sort_input_codec():
    # can't test without building a schema
    # https://github.com/graphql-python/graphene/blob/c08379ed85b2759de32777eb5dd3dca143a6d69f/graphene/types/tests/test_inputobjecttype.py#L108
    pass


def test_author_query_input():
    # can't test without building a schema
    # https://github.com/graphql-python/graphene/blob/c08379ed85b2759de32777eb5dd3dca143a6d69f/graphene/types/tests/test_inputobjecttype.py#L108
    pass
