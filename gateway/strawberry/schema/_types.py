import typing

import strawberry

if typing.TYPE_CHECKING:
    from .author import Author
    from .book import Book

AuthorType: typing.TypeAlias = typing.Annotated["Author", strawberry.lazy(".author")]
BookType: typing.TypeAlias = typing.Annotated["Book", strawberry.lazy(".book")]
