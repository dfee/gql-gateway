from typing import Optional

from graphene import ID, Argument, Field, ObjectType

from gateway.client.author import AuthorDto, AuthorPageDto
from gateway.client.book import BookDto
from gateway.context import Context, with_context
from gateway.util.goi import decode_id

from .author import Author, AuthorConnection, AuthorQueryInput
from .book import Book
from .node import Node

__all__ = ["Query"]


class Query(ObjectType):
    author = Field(Author, id=ID(required=True))
    authors = Field(AuthorConnection, input=Argument(AuthorQueryInput, required=True))
    book = Field(Book, id=ID(required=True))
    node = Field(Node, id=ID(required=True))

    @staticmethod
    @with_context
    def resolve_author(_root, _info, ctx: Context, id: str) -> Optional[AuthorDto]:
        _, _id = decode_id(id)
        return ctx.dataloaders.author_by_id.load(_id)

    @staticmethod
    @with_context
    def resolve_authors(
        _root, _info, ctx: Context, input: AuthorQueryInput
    ) -> AuthorPageDto:
        return ctx.dataloaders.author_page_by_query.load(input.to_dto())

    @staticmethod
    @with_context
    def resolve_book(_root, _info, ctx: Context, id: str) -> Optional[BookDto]:
        _, _id = decode_id(id)
        return ctx.dataloaders.book_by_id.load(_id)

    @staticmethod
    @with_context
    def resolve_node(_root, _info, ctx: Context, id: str):
        _typename, _id = decode_id(id)
        if _typename == "Author":
            return ctx.dataloaders.author_by_id.load(_id)
        if _typename == "Book":
            return ctx.dataloaders.book_by_id.load(_id)
        raise ValueError(f"Unknown type: '{_typename}'")
