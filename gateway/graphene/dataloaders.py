import typing
from dataclasses import dataclass

from promise import Promise
from promise.dataloader import DataLoader

from gateway.author import AuthorDto, AuthorService
from gateway.book import BookDto, BookService

K = typing.TypeVar("K")
T = typing.TypeVar("T")


@dataclass
class TypedDataLoader(typing.Generic[K, T]):
    dataloader: DataLoader

    def load(self, k: K) -> Promise[T]:
        return self.dataloader.load(k)

    def load_many(self, k: K) -> Promise[T]:
        return self.dataloader.load_many(k)


def build_author_by_id(
    author_service: AuthorService,
) -> TypedDataLoader[int, AuthorDto]:
    def batch_load_fn(
        keys: typing.List[int],
    ) -> Promise[typing.List[typing.Optional[AuthorDto]]]:
        results = author_service.many(keys)
        return Promise.resolve([results.get(key) for key in keys])

    return DataLoader(batch_load_fn=batch_load_fn)


def build_book_by_id(
    book_service: BookService,
) -> Promise[TypedDataLoader[int, BookDto]]:
    def batch_load_fn(
        keys: typing.List[int],
    ) -> typing.List[typing.Optional[BookDto]]:
        results = book_service.many(keys)
        return Promise.resolve([results.get(key) for key in keys])

    return DataLoader(batch_load_fn=batch_load_fn)


def build_book_by_author_id(
    book_service: BookService,
) -> Promise[TypedDataLoader[int, BookDto]]:
    def batch_load_fn(
        keys: typing.List[int],
    ) -> typing.List[typing.Optional[BookDto]]:
        results = book_service.by_author_ids(keys)
        return Promise.resolve([results.get(key) for key in keys])

    return DataLoader(batch_load_fn=batch_load_fn)


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
