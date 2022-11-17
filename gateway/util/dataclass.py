from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Type, TypeVar

T = TypeVar("T")

__all__ = [
    "b64_decode_dataclass",
    "b64_encode_dataclass",
    "json_decode_dataclass",
    "json_encode_dataclass",
]


def json_encode_dataclass(ins: T) -> str:
    return ins.to_json()


def json_decode_dataclass(cls: Type[T], value: str) -> T:
    return cls.from_json(value)


def b64_encode_dataclass(ins: T) -> str:
    return urlsafe_b64encode(json_encode_dataclass(ins).encode("utf-8")).decode("utf-8")


def b64_decode_dataclass(cls: Type[T], value: str) -> T:
    return json_decode_dataclass(cls, urlsafe_b64decode(value))
