import typing

import strawberry

from gateway.client.author import AuthorDto, AuthorQueryDto
from gateway.client.book import BookDto
from gateway.util.goi import decode_id

from ..info import Info
from ._lazy import LazyAuthor, LazyAuthorConnection, LazyAuthorQueryInput, LazyBook
from .node import Node

__all__ = ["Query"]


def resolve_author(info: Info, id: strawberry.ID) -> typing.Optional[AuthorDto]:
    _, _id = decode_id(id)
    return info.context.dataloaders.author_by_id.load(_id)


def resolve_authors(info: Info, input: LazyAuthorQueryInput) -> AuthorQueryDto:
    return info.context.dataloaders.author_page_by_query.load(input.to_dto())


def resolve_book(info: Info, id: strawberry.ID) -> typing.Optional[BookDto]:
    _, _id = decode_id(id)
    return info.context.dataloaders.book_by_id.load(_id)


@strawberry.type
class Query:
    author: typing.Optional[LazyAuthor] = strawberry.field(resolver=resolve_author)
    authors: LazyAuthorConnection = strawberry.field(resolver=resolve_authors)
    book: typing.Optional[LazyBook] = strawberry.field(resolver=resolve_book)
    node: typing.Optional[Node] = strawberry.field(resolver=Node.resolve_node)
