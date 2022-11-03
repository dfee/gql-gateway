import pytest
from graphql import ExecutionResult
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from gateway.author import AuthorDto, AuthorService
from gateway.book import BookDto, BookService
from gateway.context import Context
from gateway.generate import get_gen_path
from gateway.graphene.dataloaders import DataLoaderRegistry
from gateway.graphene.models import Author, Node
from gateway.graphene.schema import schema
from gateway.sql.context import DbContext, bootstrap, make_default_engine
from gateway.sql.fixtures import AUTHOR_ID_HERBERT, BOOK_ID_DUNE, load_fixtures
from gateway.util.graphql import gen_schema
from gateway.util.resource import load_resource as _load_resource

load_resource = lambda resource: _load_resource(__name__, resource)


@pytest.fixture
def db_context() -> DbContext:
    rv = bootstrap(engine=make_default_engine())
    with rv.sessionmaker() as session:
        load_fixtures(session)
        session.commit()
    return rv


@pytest.fixture
def session(db_context: DbContext):
    with db_context.sessionmaker() as session:
        yield session


@pytest.fixture
def author_service(session: Session) -> AuthorService:
    return AuthorService(session)


@pytest.fixture
def book_service(session: Session) -> BookService:
    return BookService(session)


@pytest.fixture
def context(author_service: AuthorService, book_service: BookService) -> Context:
    return Context(
        dataloaders=DataLoaderRegistry.setup(author_service, book_service),
        author_service=author_service,
        book_service=book_service,
    )


@pytest.fixture
def author_herbert(author_service: AuthorService) -> AuthorDto:
    return author_service.one(AUTHOR_ID_HERBERT)


@pytest.fixture
def book_dune(book_service: BookService) -> BookDto:
    return book_service.one(BOOK_ID_DUNE)


def test_schema_snapshot():
    current = gen_schema(schema.graphql_schema)
    with open(get_gen_path(), mode="r") as f:
        persisted = f.read()
    assert current == persisted


def test_query_author(
    context: Context, author_herbert: AuthorDto, book_dune: BookDto
) -> None:
    query_string = load_resource("query_author.graphql")
    variables = {"id": Node.encode_id(author_herbert)}

    result = schema.execute(
        query_string, context_value=context, variable_values=variables
    )
    assert result == ExecutionResult(
        data={
            "author": {
                "firstName": author_herbert.first_name,
                "books": [{"id": Node.encode_id(book_dune)}],
            }
        }
    )


def test_query_book(
    context: Context, author_herbert: AuthorDto, book_dune: BookDto
) -> None:
    query_string = load_resource("query_book.graphql")
    variables = {"id": Node.encode_id(book_dune)}
    result = schema.execute(
        query_string, context_value=context, variable_values=variables
    )
    assert result == ExecutionResult(
        data={
            "book": {
                "title": "Dune",
                "author": {"id": Node.encode_id(author_herbert)},
            }
        }
    )


def test_query_node__author(context: Context, author_herbert: AuthorDto) -> None:
    query_string = load_resource("query_node__author.graphql")
    variables = dict(id=Node.encode_id(author_herbert))
    result = schema.execute(
        query_string, context_value=context, variable_values=variables
    )
    assert result == ExecutionResult(
        data=dict(
            node=dict(
                __typename=Author.__name__,
                id=variables["id"],
                firstName=author_herbert.first_name,
            )
        )
    )
