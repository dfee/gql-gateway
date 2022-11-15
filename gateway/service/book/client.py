import typing
from dataclasses import dataclass

from gateway.client.book import BookClient, BookDto
from gateway.dataloader import adapt_map
from gateway.service.book import BookService


@dataclass
class NativeBookClient(BookClient):
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
