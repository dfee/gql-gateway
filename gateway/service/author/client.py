import typing
from dataclasses import dataclass

from gateway.client.author import AuthorClient, AuthorDto
from gateway.dataloader import adapt_map
from gateway.service.author import AuthorService


@dataclass
class NativeAuthorClient(AuthorClient):
    author_service: AuthorService

    @adapt_map
    def batch_load_by_id(
        self, ids: typing.Iterable[int]
    ) -> typing.Iterable[typing.Optional[AuthorDto]]:
        return self.author_service.many(ids)
