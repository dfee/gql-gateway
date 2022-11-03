import typing
from base64 import urlsafe_b64decode, urlsafe_b64encode

from gateway.author.dtos import AuthorDto
from gateway.book.dtos import BookDto

node_map = {AuthorDto: "Author", BookDto: "Book"}


def decode_id(_id: str) -> typing.Tuple[str, int]:
    _typename, _id = urlsafe_b64decode(_id).decode("utf-8").split(":")
    if _typename is None:
        raise ValueError("Could not parse ID: typename")
    if _id is None:
        raise ValueError("Could not parse ID: id")
    _id_int = int(_id, base=10)

    return (_typename, _id_int)


T = typing.TypeVar("T")


@staticmethod
def encode_id(instance: typing.Type[T]) -> str:
    _id = instance.id
    _typename = node_map.get(type(instance))
    return urlsafe_b64encode(f"{_typename}:{_id}".encode("utf-8")).decode("utf-8")
