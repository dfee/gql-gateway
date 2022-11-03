import pytest
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker as _sessionmaker

from gateway.sql.context import DbContext, bootstrap, make_default_engine
from gateway.sql.models import Author, Book


@pytest.fixture
def db_context() -> DbContext:
    return bootstrap(engine=make_default_engine())


@pytest.fixture
def session(db_context: DbContext):
    with db_context.sessionmaker() as session:
        yield session


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
