import typing
from base64 import urlsafe_b64decode, urlsafe_b64encode


def decode_id(id: str) -> typing.Tuple[str, int]:
    _typename, _id = urlsafe_b64decode(id).decode("utf-8").split(":")
    if _typename is None:
        raise ValueError("Could not parse ID: typename")
    if _id is None:
        raise ValueError("Could not parse ID: id")
    _id_int = int(_id, base=10)

    return (_typename, _id_int)


def encode_id(_typename: str, _id: typing.Any) -> str:
    return urlsafe_b64encode(f"{_typename}:{_id}".encode("utf-8")).decode("utf-8")
