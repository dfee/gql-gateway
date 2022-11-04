import typing
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import dataclass
from enum import Enum

from marshmallow_dataclass import dataclass as mm_dataclass


@dataclass
class AuthorDto:
    id: int
    first_name: str
    last_name: str


@dataclass
class CreateAuthorDto:
    first_name: str
    last_name: str
    id: typing.Optional[int] = None


T = typing.TypeVar("T")


@mm_dataclass
class AuthorCursorDto:
    """
    Everything that's required to get a page (sorting, offsets, filters, etc.)
    """

    offset: int

    def serialize(self):
        return urlsafe_b64encode(self.Schema().dumps(self).encode("utf-8"))

    @classmethod
    def deserialize(cls: typing.Type[T], value: str) -> T:
        return cls.Schema().loads(urlsafe_b64decode(value).decode("utf-8"))
