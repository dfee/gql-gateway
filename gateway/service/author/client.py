import typing
from dataclasses import dataclass

from gateway.client.author import (
    AuthorClient,
    AuthorDto,
    AuthorPage,
    AuthorQuery,
    CreateAuthorDto,
)
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
    ) -> typing.Mapping[int, AuthorDto]:
        return self.author_service.many(ids)

    @adapt_map
    def batch_load_by_query(
        self, page_queries: typing.Iterable[AuthorQuery]
    ) -> typing.Mapping[AuthorQuery, AuthorPage]:
        return self.author_service.pages(page_queries)
