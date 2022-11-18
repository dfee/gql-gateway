import typing

import strawberry

if typing.TYPE_CHECKING:
    from . import (
        Author,
        AuthorConnection,
        AuthorQueryInput,
        AuthorSortBy,
        Book,
        PageInfo,
        SortOrder,
    )

_mod = strawberry.lazy(".")

LazyAuthor: typing.TypeAlias = typing.Annotated["Author", _mod]
LazyAuthorConnection: typing.TypeAlias = typing.Annotated["AuthorConnection", _mod]
LazyAuthorQueryInput: typing.TypeAlias = typing.Annotated["AuthorQueryInput", _mod]
LazyAuthorSortBy: typing.TypeAlias = typing.Annotated["AuthorSortBy", _mod]
LazyBook: typing.TypeAlias = typing.Annotated["Book", _mod]
LazyPageInfo: typing.TypeAlias = typing.Annotated["PageInfo", _mod]
LazySortOrder: typing.TypeAlias = typing.Annotated["SortOrder", _mod]
