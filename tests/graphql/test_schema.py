import pytest
from graphql import GraphQLSchema
from pytest_snapshot.plugin import Snapshot

from gateway.client.author import AbstractAuthorClient, AuthorDto
from gateway.client.book import AbstractBookClient, BookDto
from gateway.context import Context
from gateway.dataloaders import DataLoaderRegistry
from gateway.service.author import AuthorService
from gateway.service.book import BookService
from gateway.sql.context import DbContext
from gateway.sql.fixtures import AUTHOR_ID_HERBERT, BOOK_ID_DUNE, load_fixtures
from gateway.util.goi import encode_id
from gateway.util.graphql import SCHEMA_FILENAME, pprint_schema, schema_dirpath
from gateway.util.resource import load_resource as _load_resource

load_resource = lambda resource: _load_resource(__name__, resource)


@pytest.fixture
def _fixtures(db_context: DbContext) -> None:
    with db_context.sessionmaker() as session:
        load_fixtures(session)
        session.commit()


@pytest.fixture
def context(
    author_client: AbstractAuthorClient, book_client: AbstractBookClient
) -> Context:
    return Context(
        dataloaders=DataLoaderRegistry.setup(author_client, book_client),
        author_client=author_client,
        book_client=book_client,
        request=None,
    )


@pytest.fixture
def author_herbert(_fixtures: None, author_service: AuthorService) -> AuthorDto:
    return author_service.one(AUTHOR_ID_HERBERT)


@pytest.fixture
def book_dune(_fixtures: None, book_service: BookService) -> BookDto:
    return book_service.one(BOOK_ID_DUNE)


def test_snapshot(native_schema: GraphQLSchema, snapshot: Snapshot) -> None:
    banner = "# This file is generated. Please do not edit."
    printed = pprint_schema(native_schema)
    concatenated = "\n\n".join([banner, printed])

    snapshot.snapshot_dir = schema_dirpath()
    snapshot.assert_match(concatenated, SCHEMA_FILENAME)


def test_query_author(
    execute_sync, context: Context, author_herbert: AuthorDto, book_dune: BookDto
) -> None:
    query_string = load_resource("query_author.graphql")
    variables = {"id": encode_id("Author", author_herbert.id)}

    result = execute_sync(
        query_string, context_value=context, variable_values=variables
    )
    assert result.data == {
        "author": {
            "firstName": author_herbert.first_name,
            "books": [{"id": encode_id("Book", book_dune.id)}],
        }
    }
    assert not result.errors


def test_query_book(
    execute_sync, context: Context, author_herbert: AuthorDto, book_dune: BookDto
) -> None:
    query_string = load_resource("query_book.graphql")
    variables = {"id": encode_id("Book", book_dune.id)}
    result = execute_sync(
        query_string, context_value=context, variable_values=variables
    )
    assert result.data == {
        "book": {
            "title": "Dune",
            "author": {"id": encode_id("Author", author_herbert.id)},
        }
    }


def test_query_node__author(
    execute_sync, context: Context, author_herbert: AuthorDto
) -> None:
    query_string = load_resource("query_node__author.graphql")
    variables = dict(id=encode_id("Author", author_herbert.id))
    result = execute_sync(
        query_string, context_value=context, variable_values=variables
    )
    assert result.data == {
        "node": {
            "__typename": "Author",
            "id": variables["id"],
            "firstName": author_herbert.first_name,
        }
    }
