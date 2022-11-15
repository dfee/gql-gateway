import typing
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce

from sqlalchemy import select
from sqlalchemy.orm import Session

from gateway.client.book import BookDto, CreateBookDto
from gateway.repository import models
from gateway.util.collector import Collector

from .mappers import book_model_to_dto, create_book_dto_to_model, get_book_author_id


@dataclass
class BookService:
    session: Session

    def create(self, dto: CreateBookDto) -> BookDto:
        model = create_book_dto_to_model(dto)
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return book_model_to_dto(model)

    @property
    def _query(self):
        return self.session.query(models.Book)

    def first(self, id: int) -> typing.Optional[BookDto]:
        result = self._query.filter(models.Book.id == id).first()
        return book_model_to_dto(result) if result is not None else result

    def one(self, id: int) -> BookDto:
        result = self._query.filter(models.Book.id == id).one()
        return book_model_to_dto(result)

    def many(self, ids: typing.Iterable[int]) -> typing.Mapping[int, BookDto]:
        return {
            dto.id: dto
            for dto in [
                book_model_to_dto(model)
                for model in self._query.where(models.Book.id.in_(ids)).all()
            ]
        }

    def by_author_ids(
        self, author_ids: typing.List[int]
    ) -> typing.Mapping[id, typing.Iterable[BookDto]]:
        results = self._query.filter(models.Book.author_id.in_(author_ids))
        return reduce(
            Collector(get_book_author_id, book_model_to_dto),
            results,
            defaultdict(list),
        )
