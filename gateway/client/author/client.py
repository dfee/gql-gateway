from abc import ABC, abstractmethod
from typing import Iterable, Optional

from gateway.client.author.dtos import (
    AuthorDto,
    AuthorPageDto,
    AuthorQueryDto,
    CreateAuthorDto,
)

__all__ = ["AuthorClient"]


class AuthorClient(ABC):
    @abstractmethod
    def create(self, dto: CreateAuthorDto) -> AuthorDto:
        pass

    @abstractmethod
    def batch_load_by_id(self, ids: Iterable[int]) -> Iterable[Optional[AuthorDto]]:
        pass

    @abstractmethod
    def batch_load_by_query(
        self, page_queries: Iterable[AuthorQueryDto]
    ) -> Iterable[AuthorPageDto]:
        pass
