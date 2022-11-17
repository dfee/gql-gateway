from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .dataclass import assert_b64_codec, assert_json_codec


@dataclass_json
@dataclass
class Fixture:
    id: int


FIXTURE = Fixture(1)


def test_b64_codec():
    assert_b64_codec(Fixture, FIXTURE)


def test_json_codec():
    assert_json_codec(Fixture, FIXTURE)
