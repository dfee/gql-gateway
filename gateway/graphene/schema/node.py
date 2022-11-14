import typing

from graphene import ID, Interface

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.util.goi import encode_id

T = typing.TypeVar("T")

node_map: typing.Mapping[T, str] = {AuthorDto: "Author", BookDto: "Book"}


class Node(Interface):
    id = ID(required=True)

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        import ipdb

        ipdb.set_trace()
        pass

    @staticmethod
    def resolve_mapping(instance):
        return node_map.get(instance.__class__)

    @staticmethod
    def resolve_id(parent: "Node", info):
        return encode_id(node_map.get(type(parent)), parent.id)
