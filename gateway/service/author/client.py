from dataclasses import dataclass
from typing import Iterable, Mapping

from gateway.client.author import (
    AuthorClient,
    AuthorDto,
    AuthorPageDto,
    AuthorQueryDto,
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
    def batch_load_by_id(self, ids: Iterable[int]) -> Mapping[int, AuthorDto]:
        return self.author_service.many(ids)

    def batch_load_by_query(
        self, page_queries: Iterable[AuthorQueryDto]
    ) -> Iterable[AuthorPageDto]:
        return self.author_service.pages(page_queries)
