import typing
from graphene import ObjectType, String, ID, List, Field, Interface
from gateway.repository import models, author_repository, book_repository


class Node(Interface):
    id = ID(required=True)

    @classmethod
    def resolve_type(cls, instance, info):
        if instance._typename == "Author":
            return Author
        if instance._typename == "Book":
            return Book
        raise ValueError(f"Cannot resolve type from: '{instance}'")

    def resolve_id(parent, info):
        return parent._node_id


class Author(ObjectType):
    class Meta:
        interfaces = (Node,)

    first_name = String(required=True)
    last_name = String(required=True)
    full_name = String(required=True)
    books = List(lambda: Book, required=True)

    @staticmethod
    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"

    @staticmethod
    def resolve_books(parent: models.Author, info) -> typing.List[models.Book]:
        # (actually should be going through a dataloader)
        return [book_repository.get_or_throw(book_id) for book_id in parent.book_ids]


class Book(ObjectType):
    class Meta:
        interfaces = (Node,)

    title = String(required=True)
    author = Field(lambda: Author, required=True)

    @staticmethod
    def resolve_author(parent: models.Book, info) -> models.Author:
        return author_repository.get_or_throw(parent.author_id)
