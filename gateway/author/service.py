from gateway.repository import AuthorRepository
from uuid import UUID
from typing import Mapping, Iterable, Optional
from .dtos import AuthorDto
from ..repository import Author


class AuthorService:
    """
    Boundary representing an internal facade / external µ-service.
    """

    repository: AuthorRepository

    def __init__(self, repository):
        self.repository = repository

    def many(self, ids: Iterable[UUID]) -> Mapping[UUID, AuthorDto]:
        return {
            dto.id: dto
            for dto in [
                AuthorService._author_model_to_dto(model)
                for model in self.repository.get_many(list(ids))
            ]
        }

    def first(self, id: UUID) -> Optional[AuthorDto]:
        return self.many([id]).get(id)

    def one(self, id: UUID) -> AuthorDto:
        result = self.first(id)
        if result is not None:
            return result
        raise ValueError(f"Could not load {id}")

    @staticmethod
    def _author_model_to_dto(model: Author) -> AuthorDto:
        return AuthorDto(model.id, model.first_name, model.last_name, model.book_ids)
