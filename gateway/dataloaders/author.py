import typing

from promise import Promise
from promise.dataloader import DataLoader

from gateway.author import AuthorDto, AuthorService
from gateway.book import BookDto, BookService

from .base import TypedDataLoader


def build_author_by_id(
    author_service: AuthorService,
) -> TypedDataLoader[int, AuthorDto]:
    def batch_load_fn(
        keys: typing.List[int],
    ) -> Promise[typing.List[typing.Optional[AuthorDto]]]:
        results = author_service.many(keys)
        return Promise.resolve([results.get(key) for key in keys])

    return DataLoader(batch_load_fn=batch_load_fn)
