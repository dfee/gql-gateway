import typing
from dataclasses import dataclass

from gateway.client.author import AbstractAuthorClient, AuthorDto
from gateway.client.book import AbstractBookClient, BookDto

from .base import DataLoader, FunctionalDataLoader

T = typing.TypeVar("T")


@dataclass
class DataLoaderRegistry:
    author_by_id: DataLoader[int, AuthorDto]
    book_by_id: DataLoader[int, BookDto]
    books_by_author_id: DataLoader[int, typing.List[BookDto]]

    @classmethod
    def setup(
        cls: typing.Type[T],
        author_client: AbstractAuthorClient,
        book_client: AbstractBookClient,
    ) -> T:
        return cls(
            author_by_id=FunctionalDataLoader(author_client.batch_load_by_id),
            book_by_id=FunctionalDataLoader(book_client.batch_load_by_id),
            books_by_author_id=FunctionalDataLoader(
                book_client.batch_load_by_author_id
            ),
        )
