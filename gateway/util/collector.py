import typing
from dataclasses import dataclass

K = typing.TypeVar("K")
T = typing.TypeVar("T")
U = typing.TypeVar("U")


@dataclass
class Collector(typing.Generic[K, T, U]):
    keyfn: typing.Callable[[K], T]
    transform: typing.Callable[[T], U] = lambda x: x

    def __call__(
        self, collection: typing.DefaultDict[K, T], entry: K
    ) -> typing.DefaultDict[K, T]:
        collection[self.keyfn(entry)].append(self.transform(entry))
        return collection
