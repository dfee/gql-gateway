from sqlalchemy.orm import Session

from gateway.repository.models import Author, Book


def test_author_create(session: Session):
    author = Author(first_name="Frank", last_name="Herbert")
    session.add(author)
    session.commit()

    session.refresh(author)
    assert author.id == 1


def test_book_create(session: Session):
    author = Author(first_name="Frank", last_name="Herbert")
    book = Book(title="Dune", author=author)
    session.add_all([author, book])
    session.commit()

    session.refresh(author)
    session.refresh(book)
    assert author.id == 1
    assert book.id == 1
