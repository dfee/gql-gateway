import typing
from base64 import urlsafe_b64decode, urlsafe_b64encode

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto

from .base import Interface

T = typing.TypeVar("T")


class Node(Interface, typename="Node"):
    # todo: put this into an __init_subclass__ registry
    node_map = {AuthorDto: "Author", BookDto: "Book"}

    def resolve_type(self):
        _type = self.node_map.get(type(self.value))
        if _type is not None:
            return _type
        raise ValueError(f"Cannot resolve type from: '{self.value}'")

    @staticmethod
    def decode_id(_id: str) -> typing.Tuple[str, int]:
        _typename, _id = urlsafe_b64decode(_id).decode("utf-8").split(":")
        if _typename is None:
            raise ValueError("Could not parse ID: typename")
        if _id is None:
            raise ValueError("Could not parse ID: id")
        _id_int = int(_id, base=10)

        return (_typename, _id_int)

    @classmethod
    def encode_id(cls, instance: typing.Type[T]) -> str:
        _id = instance.id
        _typename = cls.node_map.get(type(instance))
        return urlsafe_b64encode(f"{_typename}:{_id}".encode("utf-8")).decode("utf-8")
