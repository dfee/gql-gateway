from abc import ABC, abstractproperty
from dataclasses import dataclass, field
from uuid import UUID
from typing import List, Tuple, ClassVar
from base64 import b64decode, b64encode


class Node(ABC):
    @abstractproperty
    def _typename(self):
        pass

    @staticmethod
    def decode_id(_id) -> Tuple[str, str]:
        _typename, _id = b64decode(_id).decode("utf-8").split(":")
        if _typename is None:
            raise ValueError("Could not parse ID: typename")
        if _id is None:
            raise ValueError("Could not parse ID: id")
        return (_typename, _id)

    @staticmethod
    def encode_id(_typename, _id) -> str:
        return b64encode(f"{_typename}:{_id}".encode("utf-8")).decode("utf-8")

    @property
    def _node_id(self):
        return Node.encode_id(self._typename, self.id.hex)


@dataclass
class Author(Node):
    _typename: ClassVar[str] = "Author"
    id: UUID
    first_name: str
    last_name: str
    book_ids: List[UUID]


@dataclass
class Book(Node):
    _typename: ClassVar[str] = "Book"
    id: UUID
    title: str
    author_id: UUID
