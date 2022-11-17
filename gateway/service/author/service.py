from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, TypeVar

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import asc, desc

from gateway.client.author import (
    AuthorCursor,
    AuthorDto,
    AuthorPage,
    AuthorPageSortBy,
    AuthorQuery,
    AuthorSort,
    CreateAuthorDto,
)
from gateway.client.page import SortDirection
from gateway.repository import models

from .mappers import author_model_to_dto, create_author_dto_to_model

T = TypeVar("T")


# TODO: move this to a utils file. it's common.
SORT_ORDER_TO_SQLA = {
    SortDirection.ASC: asc,
    SortDirection.DESC: desc,
}

AUTHOR_PAGE_SORT_BY_TO_COLUMN_MAP = {
    # TODO: add created_at to the model :)
    AuthorPageSortBy.CREATED_AT: models.Author.id,
    AuthorPageSortBy.FIRST_NAME: models.Author.first_name,
}

# to ensure stable sorting, i.e. when no prev sorts can deterministically order
# the result set, we add a final sort that's ... deterministic.
AUTHOR_TAIL_SORT = asc(models.Author.id)

AUTHOR_LIMIT_CEILING = 100


def sorts_to_sqla(sorts: Iterable[AuthorSort]):
    _sorts = []
    for sort in sorts:
        col = AUTHOR_PAGE_SORT_BY_TO_COLUMN_MAP[sort.by]
        func = SORT_ORDER_TO_SQLA[sort.order]
        _sorts.append(func(col))
    return [*_sorts, AUTHOR_TAIL_SORT]


def page_limit_below_ceiling(limit: int) -> int:
    return min(limit, AUTHOR_LIMIT_CEILING)


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

    def pages(self, queries: Iterable[AuthorQuery]) -> Mapping[AuthorQuery, AuthorPage]:
        # alternatively, you can build this as one query in SQL.
        # remember, dataloaders are for batching <to> the remote entity.
        # it's up to the "service" layer to batch appropriately, trading off
        # complexity and performance with maintenance cost.
        return {query: self.page(query) for query in queries}

    def page(self, query: AuthorQuery) -> AuthorPage:
        sorts = sorts_to_sqla(query.sorts)
        limit = query.limit_offset.limit
        offset = query.limit_offset.offset
        nodes = [
            author_model_to_dto(model)
            for model in self._query.order_by(*sorts).limit(limit).offset(offset).all()
        ]
        return AuthorPage.from_query_and_nodes(query, nodes)
