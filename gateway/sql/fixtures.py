from sqlalchemy.orm import Session

from .models import Author, Book

# author ids
AUTHOR_ID_HERBERT = 1
AUTHOR_ID_THOMPSON = 2

# book ids
BOOK_ID_FEAR = 1
BOOK_ID_SCREWJACK = 2
BOOK_ID_DUNE = 3


def load_fixtures(session: Session) -> None:
    author_thompson = Author(
        id=AUTHOR_ID_THOMPSON,
        first_name="Hunter",
        last_name="Thompson",
    )
    author_herbert = Author(
        id=AUTHOR_ID_HERBERT, first_name="Frank", last_name="Herbert"
    )

    book_fear = Book(
        id=BOOK_ID_FEAR, title="Fear and Loathing in Las Vegas", author=author_thompson
    )
    book_screwjack = Book(
        id=BOOK_ID_SCREWJACK,
        title="Fear and Loathing in Las Vegas",
        author=author_thompson,
    )
    book_dune = Book(id=BOOK_ID_DUNE, title="Dune", author=author_herbert)

    session.add_all(
        [author_thompson, author_herbert, book_fear, book_screwjack, book_dune]
    )
