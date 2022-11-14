import pytest
from sqlalchemy.orm import Session

from gateway.service.author import AuthorService
from gateway.service.book import BookService
from gateway.sql import DbContext, bootstrap, make_default_engine


@pytest.fixture
def db_context() -> DbContext:
    return bootstrap(engine=make_default_engine())


@pytest.fixture
def session(db_context: DbContext) -> Session:
    with db_context.sessionmaker() as session:
        yield session


@pytest.fixture
def author_service(session: Session) -> AuthorService:
    return AuthorService(session)


@pytest.fixture
def book_service(session) -> BookService:
    return BookService(session)
