from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Generic, Iterable, Mapping, Optional, TypeVar, Union

from typing_extensions import TypeAlias

K = TypeVar("K")
V = TypeVar("V")

BatchLoadInput: TypeAlias = Iterable[K]
BatchLoadOutput: TypeAlias = Iterable[Optional[V]]
BatchLoadMappingOutput: TypeAlias = Iterable[Mapping[K, V]]
BatchLoadSparseOutput: TypeAlias = Iterable[V]

BatchLoadCallable: TypeAlias = Union[
    Callable[[BatchLoadInput], BatchLoadOutput],
    Callable[[Any, BatchLoadInput], BatchLoadOutput],
]
BatchLoadMappingCallable: TypeAlias = Union[
    Callable[[BatchLoadInput], BatchLoadMappingOutput],
    Callable[[Any, BatchLoadInput], BatchLoadMappingOutput],
]
BatchLoadSparseCallable: TypeAlias = Union[
    Callable[[BatchLoadInput], BatchLoadSparseOutput],
    Callable[[Any, BatchLoadInput], BatchLoadSparseOutput],
]


def adapt_map(f: BatchLoadCallable) -> BatchLoadCallable:

    """
    Wrapper for a function or method that takes an array of keys (K), and
    returns a mapping from (K -> Optional[V]).

    This method unwraps the mapping into a corresponding full result set.
    """

    @wraps(f)
    def wrapper(*args):
        keys = args[0] if len(args) == 1 else args[1]
        keymap = f(*args)
        return [keymap.get(key) for key in keys]

    return wrapper


def adapt_sparse(
    keygetter: Callable[[K], V]
) -> Callable[[BatchLoadSparseCallable], BatchLoadCallable]:
    """
    Returns a wrapper for a function or method that takes an array of keys (K),
    and returns a sparse result set of values (V).

    This method unwraps the mapping into a corresponding full result set.
    """

    def _adapt_sparse(f: BatchLoadSparseCallable) -> BatchLoadCallable:
        @wraps(f)
        def wrapper(*args):
            keys = args[0] if len(args) == 1 else args[1]
            keymap = {keygetter(v): v for v in f(*args)}
            return [keymap.get(key) for key in keys]

        return wrapper

    return _adapt_sparse


class DataLoader(ABC, Generic[K, V]):
    """
    The Abstract DataLoader provides access to `load` and `load_many`
    which are proxied into `_batch_load`.
    """

    @abstractmethod
    def _batch_load(self, keys: Iterable[K]) -> Iterable[Optional[V]]:
        pass

    def load(self, key: K) -> Optional[V]:
        """no batching"""
        return self.load_many([key])[0]

    def load_many(self, keys: Iterable[K]) -> Iterable[Optional[V]]:
        """no batching"""
        return self._batch_load(keys)

    def clear(self, key: K) -> None:
        """no-op"""
        pass

    def clear_all(self) -> None:
        """no-op"""
        pass

    def prime(self, key: K, value: V) -> None:
        """no-op"""
        pass


@dataclass
class FunctionalDataLoader(DataLoader[K, V]):
    _batch_load_fn: BatchLoadCallable

    def _batch_load(self, keys: Iterable[K]) -> Iterable[Optional[V]]:
        return self._batch_load_fn(keys)
