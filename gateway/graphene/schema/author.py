import enum
from typing import Iterable, Optional

from graphene import (
    Enum,
    Field,
    InputField,
    InputObjectType,
    Int,
    List,
    NonNull,
    ObjectType,
    String,
)

from gateway.client.author import (
    AuthorDto,
    AuthorQueryDto,
    AuthorSortByDto,
    AuthorSortDto,
)
from gateway.client.book import BookDto
from gateway.context import Context, with_context

from .node import Node
from .page import PageInfo, SortOrder, SortOrderEnum

__all__ = [
    "Author",
    "AuthorConnection",
    "AuthorQueryInput",
    "AuthorSortBy",
    "AuthorSortInput",
]


class Author(ObjectType):
    class Meta:
        interfaces = (Node,)

    first_name = String(required=True)
    last_name = String(required=True)
    full_name = String(required=True)
    books = List(NonNull("gateway.graphene.schema.book.Book"), required=True)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, AuthorDto)

    @staticmethod
    def resolve_full_name(parent: AuthorDto, info):
        return f"{parent.first_name} {parent.last_name}"

    @staticmethod
    @with_context
    def resolve_books(parent: AuthorDto, _info, ctx: Context) -> Iterable[BookDto]:
        return ctx.dataloaders.books_by_author_id.load(parent.id)


class AuthorSortBy(enum.Enum):
    CREATED_AT = "created_at"
    FIRST_NAME = "first_name"

    def to_dto(self) -> AuthorSortByDto:
        return AuthorSortByDto(self.value)

    @classmethod
    def from_dto(cls: "AuthorSortBy", dto: AuthorSortByDto) -> "AuthorSortBy":
        return cls(dto.value)


AuthorSortByEnum = Enum.from_enum(AuthorSortBy)


class AuthorSortInput(InputObjectType):
    by: AuthorSortBy = Field(AuthorSortByEnum, required=True)
    order: SortOrder = Field(SortOrderEnum, required=True)

    def to_dto(self) -> AuthorSortDto:
        return AuthorSortDto(
            by=self.by.to_dto(),
            order=self.order.to_dto(),
        )

    @classmethod
    def from_dto(cls: "AuthorSortInput", dto: AuthorSortDto) -> "AuthorSortInput":
        return cls(
            by=AuthorSortBy.from_dto(dto.by),
            order=SortOrder.from_dto(dto.order),
        )


class AuthorQueryInput(InputObjectType):
    after: Optional[str] = String(required=False)
    before: Optional[str] = String(required=False)
    first: Optional[str] = Int(required=False)
    last: Optional[str] = Int(required=False)
    sorts: Iterable[AuthorSortInput] = InputField(List(AuthorSortInput), required=False)

    def to_dto(self) -> AuthorQueryDto:
        return AuthorQueryDto(
            after=self.after,
            before=self.before,
            first=self.first,
            last=self.last,
            sorts=[sort.to_dto() for sort in self.sorts],
        )

    @classmethod
    def from_dto(cls: "AuthorQueryInput", dto: AuthorQueryDto) -> "AuthorQueryInput":
        return cls(
            after=dto.after,
            before=dto.before,
            first=dto.first,
            last=dto.last,
            sorts=[AuthorSortInput.from_dto(sort) for sort in dto.sorts],
        )


class AuthorConnection(ObjectType):
    page_info: PageInfo = Field(PageInfo)
    nodes: Iterable[Author] = List(Author)
    total_count: int = Int()
