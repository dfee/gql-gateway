from dataclasses import dataclass
from typing import Iterable, Mapping, Optional

from sqlalchemy.orm import Session

from gateway.client.author import AuthorDto, CreateAuthorDto
from gateway.sql import models

from .mappers import author_model_to_dto, create_author_dto_to_model


@dataclass
class AuthorService:
    session: Session

    def create(self, dto: CreateAuthorDto) -> AuthorDto:
        model = create_author_dto_to_model(dto)
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return author_model_to_dto(model)

    @property
    def _query(self):
        return self.session.query(models.Author)

    def first(self, id: int) -> Optional[AuthorDto]:
        result = self._query.filter(models.Author.id == id).first()
        return author_model_to_dto(result) if result is not None else result

    def one(self, id: int) -> AuthorDto:
        result = self._query.filter(models.Author.id == id).one()
        return author_model_to_dto(result)

    def many(self, ids: Iterable[int]) -> Mapping[int, AuthorDto]:
        return {
            dto.id: dto
            for dto in [
                author_model_to_dto(model)
                for model in self._query.where(models.Author.id.in_(ids)).all()
            ]
        }
