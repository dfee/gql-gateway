import typing

from promise import Promise
from promise.dataloader import DataLoader

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.service.author import AuthorService
from gateway.service.book import BookService

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
