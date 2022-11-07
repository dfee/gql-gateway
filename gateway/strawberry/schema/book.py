import typing

import strawberry
from strawberry.types import Info

from gateway.author import AuthorDto
from gateway.book import BookDto
from gateway.context import Context

from .node import Node

if typing.TYPE_CHECKING:
    from .author import Author


def resolve_author(root: BookDto, info: Info) -> "Author":
    context: Context = info.context
    return context.dataloaders.author_by_id.load(root.author_id).get()


@strawberry.type
class Book(Node):
    title: str
    author: typing.Annotated["Author", strawberry.lazy(".author")] = strawberry.field(
        resolver=resolve_author
    )

    @classmethod
    def is_type_of(cls, obj, _info) -> bool:
        return isinstance(obj, BookDto)
