import typing

from graphene import List, NonNull, ObjectType, String
from promise import Promise

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.context import Context, with_context

from .node import Node


class Author(ObjectType):
    class Meta:
        interfaces = (Node,)

    first_name = String(required=True)
    last_name = String(required=True)
    full_name = String(required=True)
    books = List(NonNull("gateway.graphene.schema.book.Book"), required=True)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, AuthorDto)

    @staticmethod
    def resolve_full_name(parent: AuthorDto, info):
        return f"{parent.first_name} {parent.last_name}"

    @staticmethod
    @with_context
    def resolve_books(
        parent: AuthorDto, _info, ctx: Context
    ) -> Promise[typing.Iterable[BookDto]]:
        return ctx.dataloaders.books_by_author_id.load(parent.id)
