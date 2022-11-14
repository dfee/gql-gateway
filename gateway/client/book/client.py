import typing
from abc import ABC, abstractmethod

from gateway.client.book.dtos import BookDto


class BookClient(ABC):
    @abstractmethod
    def batch_load(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[BookDto]]:
        pass
