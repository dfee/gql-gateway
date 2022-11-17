import pytest
from sqlalchemy.orm.exc import NoResultFound

from gateway.client.author import (
    AuthorCursor,
    AuthorDto,
    AuthorPage,
    AuthorQuery,
    CreateAuthorDto,
)
from gateway.client.page import PageInfo
from gateway.service.author import AuthorService
from gateway.util.dataclass import b64_encode_dataclass

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


def test_page(author_service: AuthorService) -> None:
    created = [
        author_service.create(create_author_dto_fixture(id)) for id in (range(5))
    ]
    query = AuthorQuery(first=3)
    page = author_service.page(query)
    assert page == AuthorPage(
        nodes=created[0:3],
        page_info=PageInfo(
            has_next_page=True,
            has_previous_page=False,
            start_cursor=None,  # todo: bug, should return regardless of next page
            end_cursor=b64_encode_dataclass(AuthorCursor(limit=3, offset=3, sorts=[])),
        ),
    )
