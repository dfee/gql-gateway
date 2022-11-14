import typing

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.util.goi import decode_id

from .base import Resolver


class Query(Resolver, typename="Query"):
    def resolve_author(self, id: str) -> typing.Optional[AuthorDto]:
        _, _id = decode_id(id)
        return self.dataloaders.author_by_id.load(_id)

    def resolve_book(self, id: str) -> typing.Optional[BookDto]:
        _, _id = decode_id(id)
        return self.dataloaders.book_by_id.load(_id)

    def resolve_node(self, id: str) -> typing.Optional[typing.Any]:
        _typename, _id = decode_id(id)
        if _typename == "Author":
            return self.dataloaders.author_by_id.load(_id)
        if _typename == "Book":
            return self.dataloaders.book_by_id.load(_id)
        raise ValueError(f"Unknown type: '{_typename}'")
