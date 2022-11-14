import typing

import strawberry

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.context import Context

from ..info import Info
from ._types import BookType
from .node import Node


def resolve_books(root: AuthorDto, info: Info) -> typing.List[BookDto]:
    return info.context.dataloaders.books_by_author_id.load(root.id)


def resolve_full_name(root: AuthorDto) -> str:
    return f"{root.first_name} {root.last_name}"


@strawberry.type
class Author(Node):
    first_name: str
    full_name: str = strawberry.field(resolver=resolve_full_name)
    last_name: str
    books: typing.List[BookType] = strawberry.field(resolver=resolve_books)

    @classmethod
    def is_type_of(cls, obj, _info) -> bool:
        return isinstance(obj, AuthorDto)
