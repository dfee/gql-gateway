from abc import ABC, abstractclassmethod, abstractproperty
from importlib.util import find_spec

from graphql import GraphQLSchema, build_schema
from graphql.pyutils import camel_to_snake

from gateway.context import Context, with_context
from gateway.core.node import decode_id, encode_id
from gateway.util.graphql import schema_filepath

with open(schema_filepath(), "r") as f:
    schema = build_schema(f.read())


class Resolver(ABC):
    @abstractclassmethod
    def typename(cls) -> str:
        pass

    @abstractclassmethod
    def query_resolvers(cls):
        # todo: use annotations
        pass

    @abstractclassmethod
    def field_resolvers(cls):
        # todo: use annotations
        pass

    @staticmethod
    def resolve_default(parent, info, **kwargs):
        field_name = info.field_name
        if hasattr(parent, field_name):
            return getattr(parent, field_name)

        field_name_snake = camel_to_snake(field_name)
        if hasattr(parent, field_name_snake):
            return getattr(parent, field_name_snake)

        return None

    @classmethod
    def bind(cls, schema: GraphQLSchema) -> None:
        for field_name, resolver in cls.query_resolvers().items():
            schema.query_type.fields[field_name].resolve = resolver

        _type = schema.get_type(cls.typename())
        for field_name, field in _type.fields.items():
            if field_name in cls.field_resolvers():
                field.resolve = cls.field_resolvers()[field_name]
                continue

            field.resolve = cls.resolve_default


class AuthorResolver(Resolver):
    @classmethod
    def typename(cls):
        return "Author"

    @classmethod
    def query_resolvers(cls):
        return {"author": cls.resolve_author}

    @classmethod
    def field_resolvers(cls):
        return {"id": cls.resolve_id}

    @staticmethod
    def resolve_id(parent, info):
        return encode_id(parent)

    @staticmethod
    @with_context
    def resolve_author(parent, info, context: Context, *, id: str):
        _, _id = decode_id(id)
        return context.dataloaders.author_by_id.load(_id).get()


AuthorResolver.bind(schema)
