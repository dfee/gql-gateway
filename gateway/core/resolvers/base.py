import typing
from abc import abstractmethod
from dataclasses import dataclass

from graphql import GraphQLSchema
from graphql.pyutils import camel_to_snake, snake_to_camel

from gateway.context import Context
from gateway.dataloader import DataLoaderRegistry


class ResolverMeta(type):
    RESOLVE_PREFIX = "resolve_"

    @staticmethod
    def resolver_to_camel_case(name: str) -> str:
        return snake_to_camel(name.split(ResolverMeta.RESOLVE_PREFIX)[1])

    @staticmethod
    def is_resolver(key: str, value: typing.Any) -> str:
        return callable(value) and key.startswith(ResolverMeta.RESOLVE_PREFIX)

    def __call__(cls, parent, info, *args, **kwargs):
        field_name = info.field_name
        field_name_sn = camel_to_snake(field_name)
        resolver_name = f"resolve_{field_name_sn}"
        # do we have a resolve method?
        if hasattr(cls, resolver_name):
            ins = super(ResolverMeta, cls).__call__(parent, info)
            method = getattr(ins, resolver_name)
            return method(*args, **kwargs)
        # does the parent object have a snake_case variant of the fieldName
        if hasattr(parent, field_name_sn):
            return getattr(parent, field_name_sn)
        # does the parent object have a fieldName that matches? else None
        return getattr(parent, field_name, None)


@dataclass
class Resolver(metaclass=ResolverMeta):
    parent: typing.Any
    info: typing.Any
    typename: typing.ClassVar[str]

    def __init_subclass__(cls, /, typename: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.typename = typename

    @classmethod
    def bind(cls, schema: GraphQLSchema) -> None:
        _type = schema.get_type(cls.typename)
        for field in _type.fields.values():
            field.resolve = cls

    @property
    def context(self) -> Context:
        return self.info.context

    @property
    def dataloaders(self) -> DataLoaderRegistry:
        return self.context.dataloaders


class InterfaceMeta(type):
    def __call__(cls, value, info, type):
        ins = super(InterfaceMeta, cls).__call__(value, info, type)
        return ins.resolve_type()


@dataclass
class Interface(metaclass=InterfaceMeta):
    value: typing.Any
    info: typing.Any
    type: typing.Any
    typename: typing.ClassVar[str]

    def __init_subclass__(cls, /, typename: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.typename = typename

    @abstractmethod
    def resolve_type(self):
        raise NotImplementedError()

    @classmethod
    def bind(cls, schema: GraphQLSchema) -> None:
        _type = schema.get_type(cls.typename)
        _type.resolve_type = cls
