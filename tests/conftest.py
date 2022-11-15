import pytest
from sqlalchemy.orm import Session

from gateway.client.author import AuthorClient
from gateway.client.book import BookClient
from gateway.repository import DbContext, bootstrap, make_default_engine
from gateway.service.author import AuthorService
from gateway.service.author.client import NativeAuthorClient
from gateway.service.book import BookService
from gateway.service.book.client import NativeBookClient


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
def author_client(author_service: AuthorService) -> AuthorClient:
    return NativeAuthorClient(author_service=author_service)


@pytest.fixture
def book_client(book_service: BookService) -> BookClient:
    return NativeBookClient(book_service=book_service)
