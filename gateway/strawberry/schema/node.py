import typing
from base64 import urlsafe_b64decode, urlsafe_b64encode

import strawberry
from strawberry.types import Info

from gateway.author import AuthorDto
from gateway.book import BookDto
from gateway.context import Context

# TODO
node_map = {AuthorDto: "Author", BookDto: "Book"}


@strawberry.interface
class Node:
    @strawberry.field
    def id(self) -> str:
        _id = self.id
        _typename = node_map.get(type(self))
        return urlsafe_b64encode(f"{_typename}:{_id}".encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_id(id: str) -> typing.Tuple[str, int]:
        _typename, _id = urlsafe_b64decode(id).decode("utf-8").split(":")
        if _typename is None:
            raise ValueError("Could not parse ID: typename")
        if _id is None:
            raise ValueError("Could not parse ID: id")
        _id_int = int(_id, base=10)

        return (_typename, _id_int)

    @staticmethod
    def resolve_node(info: Info, id: str) -> "Node":
        context: Context = info.context
        _typename, _id = Node.decode_id(id)
        if _typename == "Author":
            return context.dataloaders.author_by_id.load(_id).get()
        if _typename == "Book":
            return context.dataloaders.book_by_id.load(_id).get()
        return None
