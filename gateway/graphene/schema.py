from typing import Optional

from graphene import ID, Field, ObjectType, Schema, String
from promise import Promise

from gateway.author import AuthorDto
from gateway.book import BookDto
from gateway.util.promise import unwrap_promise

from ..context import Context, with_context
from .models import Author, Book, Node


class Query(ObjectType):
    author = Field(Author, id=ID(required=True))
    book = Field(Book, id=ID(required=True))
    node = Field(Node, id=ID(required=True))

    @staticmethod
    @with_context
    @unwrap_promise
    def resolve_author(
        _root, _info, ctx: Context, id: str
    ) -> Promise[Optional[AuthorDto]]:
        _, _id = Node.decode_id(id)
        return ctx.dataloaders.author_by_id.load(_id)

    @staticmethod
    @with_context
    @unwrap_promise
    def resolve_book(_root, _info, ctx: Context, id: str) -> Promise[Optional[BookDto]]:
        _, _id = Node.decode_id(id)
        return ctx.dataloaders.book_by_id.load(_id)

    @staticmethod
    @with_context
    @unwrap_promise
    def resolve_node(_root, _info, ctx: Context, id: str):
        _typename, _id = Node.decode_id(id)
        if _typename == "Author":
            return ctx.dataloaders.author_by_id.load(_id)
        if _typename == "Book":
            return ctx.dataloaders.book_by_id.load(_id)
        raise ValueError(f"Unknown type: '{_typename}'")


schema = Schema(query=Query)
