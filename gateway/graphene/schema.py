from uuid import UUID
from graphene import ObjectType, String, Schema, ID, Field
from gateway.repository import author_repository, book_repository, models
from .models import Author, Book, Node
from base64 import b64decode


class Query(ObjectType):
    author = Field(Author, id=ID(required=True))
    book = Field(Book, id=ID(required=True))
    node = Field(Node, id=ID(required=True))

    @staticmethod
    def resolve_author(root, info, id) -> models.Author:
        return author_repository.get_or_throw(UUID(id))

    @staticmethod
    def resolve_book(root, info, id) -> models.Book:
        return book_repository.get_or_throw(UUID(id))

    @staticmethod
    def resolve_node(root, info, id):
        _typename, _id = b64decode(id).decode().split(":")
        if _typename == "Author":
            return author_repository.get_or_throw(UUID(_id))
        if _typename == "Book":
            return book_repository.get_or_throw(UUID(_id))
        raise ValueError(f"Unknown type: '{_typename}'")


schema = Schema(query=Query)
