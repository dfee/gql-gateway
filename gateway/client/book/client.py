import typing
from dataclasses import dataclass

from gateway.client.book import AbstractBookClient, BookDto
from gateway.service.book import BookService

from ...dataloaders.base import adapt_map


@dataclass
class BookClient(AbstractBookClient):
    book_service: BookService

    @adapt_map
    def batch_load_by_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[BookDto]]:
        return self.book_service.many(ids)

    @adapt_map
    def batch_load_by_author_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[BookDto]:
        return self.book_service.by_author_ids(ids)
