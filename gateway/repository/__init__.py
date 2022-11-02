from re import I
from typing import Mapping, List
from uuid import uuid4, UUID
from .models import Author, Book

# author ids
THOMPSON_ID = uuid4()
HERBERT_ID = uuid4()

# book ids
LOATHING_ID = uuid4()
SCREWJACK_ID = uuid4()
DUNE_ID = uuid4()

THOMPSON = Author(
    THOMPSON_ID,
    "Hunter",
    "Thompson",
    [LOATHING_ID, SCREWJACK_ID],
)
HERBERT = Author(HERBERT_ID, "Frank", "Herbert", [DUNE_ID])

LOATHING = Book(LOATHING_ID, "Fear and Loathing in Las Vegas", THOMPSON_ID)
SCREWJACK = Book(SCREWJACK_ID, "Fear and Loathing in Las Vegas", THOMPSON_ID)
DUNE = Book(DUNE_ID, "Dune", HERBERT_ID)


class AuthorRepository:
    authors: Mapping[UUID, Author] = {
        author.id: author for author in [THOMPSON, HERBERT]
    }

    def get_or_throw(self, id: UUID) -> Author:
        author = self.authors.get(id)
        if author is None:
            raise TypeError(f"Author not found: '{id}'")
        return author


author_repository = AuthorRepository()


class BookRepository:
    books: Mapping[UUID, Book] = {book.id: book for book in [LOATHING, SCREWJACK, DUNE]}

    def get_or_throw(self, id: UUID) -> Book:
        book = self.books.get(id)
        if book is None:
            raise TypeError(f"Book not found: '{id}'")
        return book


book_repository = BookRepository()
