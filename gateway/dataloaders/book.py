import typing

from promise import Promise
from promise.dataloader import DataLoader

from gateway.author import AuthorDto, AuthorService
from gateway.book import BookDto, BookService

from .base import TypedDataLoader


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
