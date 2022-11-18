import pytest

from gateway.graphene.schema.page import PageInfo, SortOrder


def test_page_info_codec():
    ins = PageInfo(
        has_next_page=True,
        has_previous_page=True,
        start_cursor="start",
        end_cursor="end",
    )
    assert PageInfo.from_dto(ins.to_dto()) == ins


@pytest.mark.parametrize(("member",), [[m] for m in SortOrder])
def test_author_sort_by_codec(member: SortOrder) -> None:
    assert SortOrder.from_dto(member.to_dto()) == member
