import typing

import strawberry
from strawberry.types import Info

from gateway.author import AuthorDto
from gateway.book import BookDto
from gateway.context import Context

from .node import Node

if typing.TYPE_CHECKING:
    from .book import Book


def resolve_books(root: AuthorDto, info: Info) -> typing.List[BookDto]:
    context: Context = info.context
    return context.dataloaders.book_by_author_id.load(root.id).get()


@strawberry.type
class Author(Node):
    first_name: str
    last_name: str
    books: typing.List[
        typing.Annotated["Book", strawberry.lazy(".book")]
    ] = strawberry.field(resolver=resolve_books)

    @classmethod
    def is_type_of(cls, obj, _info) -> bool:
        return isinstance(obj, AuthorDto)
