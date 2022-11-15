import typing
from abc import ABC, abstractmethod

from gateway.client.author.dtos import AuthorDto, CreateAuthorDto


class AuthorClient(ABC):
    @abstractmethod
    def create(self, dto: CreateAuthorDto) -> AuthorDto:
        pass

    @abstractmethod
    def batch_load_by_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[AuthorDto]]:
        pass
