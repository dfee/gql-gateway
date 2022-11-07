import pytest
from sqlalchemy.orm.exc import NoResultFound

from gateway.author.dtos import AuthorDto, CreateAuthorDto
from gateway.author.service import AuthorService
from gateway.sql import DbContext, bootstrap, make_default_engine

CREATE_AUTHOR_DTO_1 = CreateAuthorDto(first_name="Neil", last_name="Stephenson")


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
