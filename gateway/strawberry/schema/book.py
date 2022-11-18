import typing

import strawberry

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.context import Context

from ..info import Info
from ._lazy import LazyAuthor
from .node import Node

__all__ = [
    "Book",
]


def resolve_author(root: BookDto, info: Info) -> AuthorDto:
    return info.context.dataloaders.author_by_id.load(root.author_id)


@strawberry.type
class Book(Node):
    title: str
    author: LazyAuthor = strawberry.field(resolver=resolve_author)

    @classmethod
    def is_type_of(cls, obj, _info) -> bool:
        return isinstance(obj, BookDto)
