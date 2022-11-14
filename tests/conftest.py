import pytest
from sqlalchemy.orm import Session

from gateway.client.author import AbstractAuthorClient
from gateway.client.author.client import AuthorClient
from gateway.client.book import AbstractBookClient
from gateway.client.book.client import BookClient
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


@pytest.fixture
def author_client(author_service: AuthorService) -> AbstractAuthorClient:
    return AuthorClient(author_service=author_service)


@pytest.fixture
def book_client(book_service: BookService) -> AbstractBookClient:
    return BookClient(book_service=book_service)
