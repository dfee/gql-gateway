import typing

import strawberry
from strawberry.types import Info

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.context import Context

from ._types import AuthorType
from .node import Node

if typing.TYPE_CHECKING:
    from .author import Author


def resolve_author(root: BookDto, info: Info) -> "Author":
    context: Context = info.context
    return context.dataloaders.author_by_id.load(root.author_id).get()


@strawberry.type
class Book(Node):
    title: str
    author: AuthorType = strawberry.field(resolver=resolve_author)

    @classmethod
    def is_type_of(cls, obj, _info) -> bool:
        return isinstance(obj, BookDto)
