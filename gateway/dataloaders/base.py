import typing
from dataclasses import dataclass

from promise import Promise
from promise.dataloader import DataLoader

K = typing.TypeVar("K")
T = typing.TypeVar("T")


@dataclass
class TypedDataLoader(typing.Generic[K, T]):
    dataloader: DataLoader

    def load(self, k: K) -> Promise[T]:
        return self.dataloader.load(k)

    def load_many(self, k: K) -> Promise[T]:
        return self.dataloader.load_many(k)
