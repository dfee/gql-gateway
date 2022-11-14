from gateway.client.author import AuthorDto

from .base import Resolver
from .node import Node


class Author(Resolver, typename="Author"):
    @property
    def _parent(self) -> AuthorDto:
        # typing convenience
        return self.parent

    def resolve_id(self):
        return Node.encode_id(self.parent)

    def resolve_books(self):
        return self.dataloaders.book_by_author_id.load(self._parent.id).get()

    def resolve_full_name(self):
        return f"{self._parent.first_name} {self._parent.last_name}"
