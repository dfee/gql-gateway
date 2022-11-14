import typing

import strawberry

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.util.goi import decode_id

from ..info import Info
from ._types import AuthorType, BookType
from .node import Node


def resolve_author(info: Info, id: strawberry.ID) -> typing.Optional[AuthorDto]:
    _, _id = decode_id(id)
    return info.context.dataloaders.author_by_id.load(_id)


def resolve_book(info: Info, id: strawberry.ID) -> typing.Optional[BookDto]:
    _, _id = decode_id(id)
    return info.context.dataloaders.book_by_id.load(_id)


@strawberry.type
class Query:
    author: typing.Optional[AuthorType] = strawberry.field(resolver=resolve_author)
    book: typing.Optional[BookType] = strawberry.field(resolver=resolve_book)
    node: typing.Optional[Node] = strawberry.field(resolver=Node.resolve_node)
