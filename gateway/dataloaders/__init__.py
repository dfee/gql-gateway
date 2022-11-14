import typing
from dataclasses import dataclass

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.service.author import AuthorService
from gateway.service.book import BookService

from .author import build_author_by_id
from .base import TypedDataLoader
from .book import build_book_by_author_id, build_book_by_id

K = typing.TypeVar("K")
T = typing.TypeVar("T")


@dataclass
class DataLoaderRegistry:
    author_by_id: TypedDataLoader[int, AuthorDto]
    book_by_author_id: TypedDataLoader[int, BookDto]
    book_by_id: TypedDataLoader[int, BookDto]

    @classmethod
    def setup(
        cls: typing.Type[T], author_service: AuthorService, book_service: BookService
    ) -> T:
        return cls(
            author_by_id=build_author_by_id(author_service),
            book_by_author_id=build_book_by_author_id(book_service),
            book_by_id=build_book_by_id(book_service),
        )
