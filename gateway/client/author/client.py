import typing
from abc import ABC, abstractmethod

from gateway.client.author.dtos import AuthorDto


class AuthorClient(ABC):
    @abstractmethod
    def batch_load_by_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[AuthorDto]]:
        pass
