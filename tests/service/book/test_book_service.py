import pytest
from sqlalchemy.orm.exc import NoResultFound

from gateway.client.author import AuthorDto, CreateAuthorDto
from gateway.client.book import BookDto, CreateBookDto
from gateway.service.author import AuthorService
from gateway.service.book import BookService

CREATE_AUTHOR_DTO_1 = CreateAuthorDto(id=1, first_name="Neil", last_name="Stephenson")
CREATE_BOOK_DTO_1 = CreateBookDto(title="Snow Crash", author_id=CREATE_AUTHOR_DTO_1.id)


@pytest.fixture
def author1(author_service: AuthorService) -> AuthorDto:
    return author_service.create(CREATE_AUTHOR_DTO_1)


@pytest.fixture
def book1(book_service: BookService, author1: AuthorDto) -> BookDto:
    return book_service.create(CREATE_BOOK_DTO_1)


def test_create(book_service: BookService, author1: AuthorDto) -> None:
    dto = book_service.create(CREATE_BOOK_DTO_1)
    assert dto == BookDto(
        id=1, author_id=CREATE_BOOK_DTO_1.author_id, title=CREATE_BOOK_DTO_1.title
    )


def test_one(book_service: BookService, book1: BookDto) -> None:
    result = book_service.one(book1.id)
    assert result == book1


def test_one_fail(book_service: BookService) -> None:
    with pytest.raises(NoResultFound):
        book_service.one(1)


def test_first(book_service: BookService, book1: BookDto) -> None:
    result = book_service.first(book1.id)
    assert result == book1


def test_first_none(book_service: BookService) -> None:
    assert book_service.first(1) is None


def test_many(book_service: BookService, book1: BookDto) -> None:
    result = book_service.many([book1.id])
    assert result == {book1.id: book1}


def test_many_none(book_service: BookService) -> None:
    assert book_service.many([1]) == {}


def test_by_author_ids(book_service: BookService, book1: BookDto) -> None:
    result = book_service.by_author_ids([book1.id])
    assert result == {book1.author_id: [book1]}
