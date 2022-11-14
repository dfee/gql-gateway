import typing

from promise import Promise
from promise.dataloader import DataLoader

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.service.author import AuthorService
from gateway.service.book import BookService

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
