from typing import Any, Mapping, Type

from graphene import ID, Interface

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.util.goi import encode_id

__all__ = ["Node"]

node_map: Mapping[Type[Any], str] = {
    AuthorDto: "Author",
    BookDto: "Book",
}


class Node(Interface):
    id = ID(required=True)

    @staticmethod
    def resolve_mapping(instance):
        return node_map.get(instance.__class__)

    @staticmethod
    def resolve_id(parent: "Node", info):
        return encode_id(node_map.get(type(parent)), parent.id)
