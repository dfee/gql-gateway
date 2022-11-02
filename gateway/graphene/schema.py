from uuid import UUID
from typing import Container, Optional
from graphene import ObjectType, String, Schema, ID, Field
from gateway.author import AuthorDto
from gateway.book import BookDto
from .models import Author, Book, Node
from base64 import b64decode
from .context import Context, with_context, as_context


class Query(ObjectType):
    author = Field(Author, id=ID(required=True))
    book = Field(Book, id=ID(required=True))
    node = Field(Node, id=ID(required=True))

    @staticmethod
    @with_context
    async def resolve_author(
        _root, _info, ctx: Context, id: str
    ) -> Optional[AuthorDto]:
        return await ctx.author_data_loader.load(UUID(id))

    @staticmethod
    @with_context
    async def resolve_book(_root, _info, ctx: Context, id: str) -> Optional[BookDto]:
        return await ctx.book_data_loader.load(UUID(id))

    @staticmethod
    @with_context
    async def resolve_node(_root, _info, ctx: Context, id: str):
        _typename, _id = Node.decode_id(id)
        if _typename == "Author":
            return await ctx.author_data_loader.load(UUID(_id))
        if _typename == "Book":
            return await ctx.book_data_loader.load(UUID(_id))
        raise ValueError(f"Unknown type: '{_typename}'")


schema = Schema(query=Query)
