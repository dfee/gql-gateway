from dataclasses import dataclass
from typing import Iterable, Mapping, Optional

import pytest

from gateway.dataloaders import (
    DataLoader,
    FunctionalDataLoader,
    adapt_map,
    adapt_sparse,
)


@dataclass
class Fixture:
    id: int


REGISTRY: Mapping[int, Fixture] = {i: Fixture(i) for i in range(0, 3)}


def assert_load_many(dataloader: DataLoader[int, Fixture]) -> None:
    assert dataloader.load_many(range(0, 5)) == [
        Fixture(0),
        Fixture(1),
        Fixture(2),
        None,
        None,
    ]


@dataclass
class FixtureDataLoader(DataLoader[int, Fixture]):
    """
    Takes state (the registry) and returns a full result array.

    > dataloader._batch_load([0, 1, 2, 3, 4])
    [Fixture(0), Fixture(1), Fixture(2), None, None]

    > dataloader.load_many([0, 1, 2, 3, 4])
    [Fixture(0), Fixture(1), Fixture(2), None, None]
    """

    registry: Mapping[int, Fixture]

    def _batch_load(self, keys: Iterable[int]) -> Iterable[Optional[Fixture]]:
        return [self.registry.get(key) for key in keys]


@dataclass
class FixtureDataLoader_AdaptingMap(DataLoader[int, Fixture]):
    """
    Takes state (the registry) and returns a mapping.
    Note, the `adapt_map` impl. handles missing keys, too.

    > dataloader._batch_load([0, 1, 2, 3, 4])
    {0: Fixture(0), 1: Fixture(1), 2: Fixture(2), 3: None, 4: None}

    > dataloader.load_many([0, 1, 2, 3, 4])
    [Fixture(0), Fixture(1), Fixture(2), None, None]
    """

    registry: Mapping[int, Fixture]

    @adapt_map
    def _batch_load(self, keys: Iterable[int]) -> Mapping[int, Fixture]:
        return {key: self.registry.get(key) for key in keys}


@dataclass
class FixtureDataLoader_AdaptingSparse(DataLoader[int, Fixture]):
    """
    Takes state (the registry) and returns a full result array.

    > dataloader._batch_load([0, 1, 2, 3, 4])
    [Foo(1), Foo(2), Foo(3)]

    > dataloader.load_many([0, 1, 2, 3, 4])
    [Fixture(0), Fixture(1), Fixture(2), None, None]
    """

    registry: Mapping[int, Fixture]

    @adapt_sparse(lambda fixture: fixture.id)
    def _batch_load(self, keys: Iterable[int]) -> Iterable[Fixture]:
        return [
            fixture for fixture in [self.registry.get(key) for key in keys] if fixture
        ]


@dataclass
class FixtureDataLoader_Functional:
    """
    Does not subclass DataLoader, but instead supplies its `batch_load`
    method as an argument to `FunctionalDataLoader`
    """

    registry: Mapping[int, Fixture]

    def batch_load(self, keys: Iterable[int]) -> Iterable[Optional[Fixture]]:
        return [self.registry.get(key) for key in keys]


def batch_load_fn(keys: Iterable[int]) -> Iterable[Optional[Fixture]]:
    """
    Does not subclass DataLoader, but instead is an argument to
    `FunctionalDataLoader`
    """

    return [REGISTRY.get(key) for key in keys]


@pytest.mark.parametrize(
    "dataloader_cls",
    [
        FixtureDataLoader(REGISTRY),
        FixtureDataLoader_AdaptingMap(REGISTRY),
        FixtureDataLoader_AdaptingSparse(REGISTRY),
        FunctionalDataLoader(FixtureDataLoader_Functional(REGISTRY).batch_load),
        FunctionalDataLoader(batch_load_fn),
    ],
)
def test_without_wrappers(dataloader_cls) -> None:
    assert_load_many(dataloader_cls)
