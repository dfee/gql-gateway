import typing

from gateway.author.dtos import AuthorDto
from gateway.book.dtos import BookDto

from .base import Resolver
from .node import Node


class Query(Resolver, typename="Query"):
    def resolve_author(self, id: str) -> typing.Optional[AuthorDto]:
        _, _id = Node.decode_id(id)
        return self.dataloaders.author_by_id.load(_id).get()

    def resolve_book(self, id: str) -> typing.Optional[BookDto]:
        _, _id = Node.decode_id(id)
        return self.dataloaders.book_by_id.load(_id).get()

    def resolve_node(self, id: str) -> typing.Optional[typing.Any]:
        _typename, _id = Node.decode_id(id)
        if _typename == "Author":
            return self.dataloaders.author_by_id.load(_id).get()
        if _typename == "Book":
            return self.dataloaders.book_by_id.load(_id).get()
        raise ValueError(f"Unknown type: '{_typename}'")
