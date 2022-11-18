from graphene import Field, ObjectType, String

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.context import Context, with_context

from .node import Node

__all__ = ["Book"]


class Book(ObjectType):
    class Meta:
        interfaces = (Node,)

    title = String(required=True)
    author = Field("gateway.graphene.schema.author.Author", required=True)

    @staticmethod
    @with_context
    def resolve_author(parent: BookDto, _info, context: Context) -> AuthorDto:
        return context.dataloaders.author_by_id.load(parent.author_id)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, BookDto)
