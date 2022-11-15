import typing
from dataclasses import dataclass

from gateway.client.author import AuthorClient, AuthorDto, CreateAuthorDto
from gateway.dataloader import adapt_map
from gateway.service.author import AuthorService


@dataclass
class NativeAuthorClient(AuthorClient):
    author_service: AuthorService

    def create(self, dto: CreateAuthorDto) -> AuthorDto:
        return self.author_service.create(dto)

    @adapt_map
    def batch_load_by_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[AuthorDto]]:
        return self.author_service.many(ids)
