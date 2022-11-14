import typing

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.util.goi import encode_id

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

    @classmethod
    def encode_id(cls, instance: typing.Type[T]) -> str:
        return encode_id(cls.node_map.get(type(instance)), instance.id)
