import pytest
from sqlalchemy.orm.exc import NoResultFound

from gateway.client.author import (
    AuthorCursorDto,
    AuthorDto,
    AuthorPageDto,
    AuthorQueryDto,
    CreateAuthorDto,
)
from gateway.client.page import PageInfo
from gateway.service.author import AuthorService

CREATE_AUTHOR_DTO_1 = CreateAuthorDto(first_name="Neil", last_name="Stephenson")


def create_author_dto_fixture(id: int) -> CreateAuthorDto:
    return CreateAuthorDto(id=id, first_name=f"fname_{id}", last_name=f"lname_{id}")


@pytest.fixture
def author1(author_service: AuthorService) -> AuthorDto:
    return author_service.create(CREATE_AUTHOR_DTO_1)


def test_create(author_service: AuthorService) -> None:
    dto = author_service.create(CREATE_AUTHOR_DTO_1)
    assert dto == AuthorDto(
        id=1,
        first_name=CREATE_AUTHOR_DTO_1.first_name,
        last_name=CREATE_AUTHOR_DTO_1.last_name,
    )


def test_one(author_service: AuthorService, author1: AuthorDto) -> None:
    result = author_service.one(author1.id)
    assert result == author1


def test_one_fail(author_service: AuthorService) -> None:
    with pytest.raises(NoResultFound):
        author_service.one(1)


def test_first(author_service: AuthorService, author1: AuthorDto) -> None:
    result = author_service.first(author1.id)
    assert result == author1


def test_first_none(author_service: AuthorService) -> None:
    assert author_service.first(1) is None


def test_many(author_service: AuthorService, author1: AuthorDto) -> None:
    result = author_service.many([author1.id])
    assert result == {author1.id: author1}


def test_many_none(author_service: AuthorService) -> None:
    assert author_service.many([1]) == {}


def test_pages(author_service: AuthorService) -> None:
    creation_count = 5
    created = [
        author_service.create(create_author_dto_fixture(id))
        for id in (range(1, creation_count + 1))
    ]

    query0 = AuthorQueryDto(first=3)
    expected0 = AuthorPageDto(
        nodes=created[0:3],
        page_info=PageInfo(
            has_next_page=True,
            has_previous_page=False,
            start_cursor=query0.preferred_cursor.replace_offset(1).encode(),
            end_cursor=query0.preferred_cursor.replace_offset(3).encode(),
        ),
        total_count=creation_count,
    )

    query1 = AuthorQueryDto(first=3, after=AuthorCursorDto(offset=1).encode())
    expected1 = AuthorPageDto(
        nodes=created[1:4],
        page_info=PageInfo(
            has_next_page=True,
            has_previous_page=True,
            start_cursor=query1.preferred_cursor.replace_offset(2).encode(),
            end_cursor=query1.preferred_cursor.replace_offset(4).encode(),
        ),
        total_count=creation_count,
    )

    query2 = AuthorQueryDto(last=3, before=AuthorCursorDto(offset=5).encode())
    expected2 = AuthorPageDto(
        nodes=created[1:4],
        page_info=PageInfo(
            has_next_page=True,
            has_previous_page=True,
            start_cursor=query2.preferred_cursor.replace_offset(2).encode(),
            end_cursor=query2.preferred_cursor.replace_offset(4).encode(),
        ),
        total_count=creation_count,
    )

    queries = [query0, query1, query2]
    expected = [expected0, expected1, expected2]
    actual = author_service.pages(queries)
    assert actual == expected
