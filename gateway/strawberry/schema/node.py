import strawberry

from gateway.client.author import AuthorDto
from gateway.client.book import BookDto
from gateway.util.goi import decode_id, encode_id

from ..info import Info

# TODO
node_map = {AuthorDto: "Author", BookDto: "Book"}

__all__ = [
    "Node",
]


@strawberry.interface
class Node:
    @strawberry.field
    def id(self) -> strawberry.ID:
        return encode_id(node_map.get(type(self)), _id=self.id)

    @staticmethod
    def resolve_node(info: Info, id: strawberry.ID) -> "Node":
        _typename, _id = decode_id(id)
        if _typename == "Author":
            return info.context.dataloaders.author_by_id.load(_id)
        if _typename == "Book":
            return info.context.dataloaders.book_by_id.load(_id)
        return None
