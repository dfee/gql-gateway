import typing

import strawberry
from strawberry.types import Info

from gateway.author import AuthorDto
from gateway.book import BookDto
from gateway.context import Context

from ._types import AuthorType, BookType
from .node import Node


def resolve_author(info: Info, id: str) -> typing.Optional[AuthorDto]:
    context: Context = info.context
    _typename, _id = Node.decode_id(id)
    return context.dataloaders.author_by_id.load(_id).get()


def resolve_book(info: Info, id: str) -> typing.Optional[BookDto]:
    context: Context = info.context
    _typename, _id = Node.decode_id(id)
    return context.dataloaders.book_by_id.load(_id).get()


@strawberry.type
class Query:
    author: typing.Optional[AuthorType] = strawberry.field(resolver=resolve_author)
    book: typing.Optional[BookType] = strawberry.field(resolver=resolve_book)
    node: typing.Optional[Node] = strawberry.field(resolver=Node.resolve_node)
