from gateway.repository import BookRepository
from uuid import UUID
from typing import Mapping, Iterable, Optional
from .dtos import BookDto
from ..repository import Book


class BookService:
    """
    Boundary representing an internal facade / external µ-service.
    """

    repository: BookRepository

    def __init__(self, repository):
        self.repository = repository

    def many(self, ids: Iterable[UUID]) -> Mapping[UUID, BookDto]:
        return {
            dto.id: dto
            for dto in [
                BookService._author_model_to_dto(model)
                for model in self.repository.get_many(list(ids))
            ]
        }

    def first(self, id: UUID) -> Optional[BookDto]:
        return self.many([id]).get(id)

    def one(self, id: UUID) -> BookDto:
        result = self.first(id)
        if result is not None:
            return result
        raise ValueError(f"Could not load {id}")

    @staticmethod
    def _author_model_to_dto(model: Book) -> BookDto:
        return BookDto(model.id, model.title, model.author_id)
