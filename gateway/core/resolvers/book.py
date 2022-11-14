from gateway.client.book import BookDto

from .base import Resolver
from .node import Node


class Book(Resolver, typename="Book"):
    @property
    def _parent(self) -> BookDto:
        # typing convenience
        return self.parent

    def resolve_id(self):
        return Node.encode_id(self.parent)

    def resolve_author(self):
        return self.dataloaders.author_by_id.load(self._parent.author_id).get()
