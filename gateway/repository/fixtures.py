from sqlalchemy.orm import Session

from .models import Author, Book

# author ids
AUTHOR_ID_HERBERT = 1
AUTHOR_ID_THOMPSON = 2
AUTHOR_ID_VONNEGUT = 3

# book ids
BOOK_ID_FEAR = 1
BOOK_ID_SCREWJACK = 2
BOOK_ID_DUNE = 3
BOOK_ID_BREAKFAST = 4


def load_fixtures(session: Session) -> None:
    # hunter s. thompson
    author_thompson = Author(
        id=AUTHOR_ID_THOMPSON,
        first_name="Hunter",
        last_name="Thompson",
    )
    book_fear = Book(
        id=BOOK_ID_FEAR,
        title="Fear and Loathing in Las Vegas",
        author=author_thompson,
    )
    book_screwjack = Book(
        id=BOOK_ID_SCREWJACK,
        title="Fear and Loathing in Las Vegas",
        author=author_thompson,
    )

    # frank herbert
    author_herbert = Author(
        id=AUTHOR_ID_HERBERT,
        first_name="Frank",
        last_name="Herbert",
    )
    book_dune = Book(
        id=BOOK_ID_DUNE,
        title="Dune",
        author=author_herbert,
    )

    # kurt vonnegut
    author_vonnegut = Author(
        id=AUTHOR_ID_VONNEGUT,
        first_name="Kurt",
        last_name="Vonnegut",
    )
    book_breakfast = Book(
        id=BOOK_ID_BREAKFAST,
        title="Breakfast of Champions",
        author=author_vonnegut,
    )

    session.add_all(
        [
            author_thompson,
            author_herbert,
            author_vonnegut,
            book_fear,
            book_screwjack,
            book_dune,
            book_breakfast,
        ]
    )
