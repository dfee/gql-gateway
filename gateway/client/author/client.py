import typing
from dataclasses import dataclass

from gateway.client.author import AbstractAuthorClient, AuthorDto
from gateway.service.author import AuthorService

from ...dataloaders.base import adapt_map


@dataclass
class AuthorClient(AbstractAuthorClient):
    author_service: AuthorService

    @adapt_map
    def batch_load_by_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[AuthorDto]]:
        return self.author_service.many(ids)
