from aiodataloader import DataLoader
import typing
from uuid import UUID

from gateway.author import AuthorDto, AuthorService
from gateway.book import BookDto, BookService


class AuthorBatchLoader:
    # TODO: factory method for batch_load would be good enough
    def __init__(self, author_service: AuthorService):
        self.author_service = author_service

    async def batch_load(
        self, keys: typing.List[UUID]
    ) -> typing.List[typing.Optional[AuthorDto]]:
        results = self.author_service.many(keys)
        return [results.get(key) for key in keys]

    @classmethod
    def as_dataloader(cls, author_service: AuthorService) -> DataLoader:
        return DataLoader(batch_load_fn=cls(author_service).batch_load)


class BookBatchLoader:
    # TODO: factory method for batch_load would be good enough
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    async def batch_load(
        self, keys: typing.List[UUID]
    ) -> typing.List[typing.Optional[BookDto]]:
        results = self.book_service.many(keys)
        return [results.get(key) for key in keys]

    @classmethod
    def as_dataloader(cls, book_service: BookService) -> DataLoader:
        return DataLoader(batch_load_fn=cls(book_service).batch_load)
