from typing import Type, TypeVar

from gateway.util.dataclass import (
    b64_decode_dataclass,
    b64_encode_dataclass,
    json_decode_dataclass,
    json_encode_dataclass,
)

T = TypeVar("T")


def assert_b64_codec(cls: Type[T], value: T) -> None:
    assert b64_decode_dataclass(cls, b64_encode_dataclass(value))


def assert_json_codec(cls: Type[T], value: T) -> None:
    assert json_decode_dataclass(cls, json_encode_dataclass(value))
