import typing
from base64 import urlsafe_b64decode, urlsafe_b64encode
from functools import cache

from graphene import ID, Field, Interface, List, NonNull, ObjectType, String
from promise import Promise

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.context import Context, with_context
from gateway.util.classproperty import classproperty
from gateway.util.promise import unwrap_promise


class Node(Interface):
    id = ID(required=True)

    @staticmethod
    def resolve_mapping(instance):
        # TODO: better to build this using something like __subclasshook__
        node_map = {AuthorDto: Author, BookDto: Book}
        return node_map.get(instance.__class__)

    @classproperty
    @cache
    def node_map(cls):
        # TODO: memoize, build up during class creation... __subclasshook__
        return {AuthorDto: Author, BookDto: Book}

    @classmethod
    def resolve_type(cls, instance, info):
        graphene_type = cls.node_map.get(type(instance))
        if graphene_type is not None:
            return graphene_type
        raise ValueError(f"Cannot resolve type from: '{instance}'")

    @classmethod
    def resolve_id(cls, parent, info):
        return cls.encode_id(parent)

    @staticmethod
    def decode_id(_id) -> typing.Tuple[str, int]:
        _typename, _id = urlsafe_b64decode(_id).decode("utf-8").split(":")
        if _typename is None:
            raise ValueError("Could not parse ID: typename")
        if _id is None:
            raise ValueError("Could not parse ID: id")
        _id_int = int(_id, base=10)

        return (_typename, _id_int)

    @staticmethod
    def encode_id(instance) -> str:
        _id = instance.id
        _typename = Node.node_map.get(type(instance)).__name__
        return urlsafe_b64encode(f"{_typename}:{_id}".encode("utf-8")).decode("utf-8")


class Author(ObjectType):
    class Meta:
        interfaces = (Node,)

    first_name = String(required=True)
    last_name = String(required=True)
    full_name = String(required=True)
    books = List(NonNull(lambda: Book), required=True)

    @staticmethod
    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"

    @staticmethod
    @with_context
    @unwrap_promise
    def resolve_books(
        parent: AuthorDto, _info, ctx: Context
    ) -> Promise[typing.Iterable[BookDto]]:
        return ctx.dataloaders.book_by_author_id.load(parent.id)


class Book(ObjectType):
    class Meta:
        interfaces = (Node,)

    title = String(required=True)
    author = Field(lambda: Author, required=True)

    @staticmethod
    @with_context
    @unwrap_promise
    def resolve_author(parent: BookDto, _info, context: Context) -> Promise[AuthorDto]:
        return context.dataloaders.author_by_id.load(parent.author_id)
