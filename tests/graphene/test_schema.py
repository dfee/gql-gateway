from graphql import ExecutionResult
from gateway.graphene.context import Context
from gateway.graphene.models import Node, Author
from gateway.graphene.schema import schema
from gateway.author import AuthorService
from gateway.book import BookService
from gateway.graphene.dataloaders import AuthorBatchLoader, BookBatchLoader
from gateway.repository import HERBERT_ID, DUNE_ID
import pytest

from gateway.util.resource import load_resource as _load_resource
from gateway.util.graphql import gen_schema
from gateway.generate import get_gen_path

load_resource = lambda resource: _load_resource(__name__, resource)


@pytest.fixture
def author_service() -> AuthorService:
    from gateway.repository import AuthorRepository

    return AuthorService(AuthorRepository())


@pytest.fixture
def book_service() -> BookService:
    from gateway.repository import BookRepository

    return BookService(BookRepository())


@pytest.fixture
def context(author_service: AuthorService, book_service: BookService) -> Context:
    return Context(
        AuthorBatchLoader.as_dataloader(author_service),
        BookBatchLoader.as_dataloader(book_service),
        author_service,
        book_service,
    )


def test_schema_snapshot():
    current = gen_schema(schema.graphql_schema)
    with open(get_gen_path(), mode="r") as f:
        persisted = f.read()
    assert current == persisted


@pytest.mark.asyncio
async def test_query_author(context: Context):
    herbert = context.author_service.one(HERBERT_ID)
    dune = context.book_service.one(DUNE_ID)

    query_string = load_resource("query_author.graphql")
    variables = {"id": herbert.id.hex}

    result = await schema.execute_async(
        query_string, context_value=context, variable_values=variables
    )
    assert result == ExecutionResult(
        data={
            "author": {
                "firstName": herbert.first_name,
                "books": [{"id": Node.encode_id(dune)}],
            }
        }
    )


@pytest.mark.asyncio
async def test_query_book(context: Context):
    herbert = context.author_service.one(HERBERT_ID)
    dune = context.book_service.one(DUNE_ID)

    query_string = load_resource("query_book.graphql")
    variables = {"id": dune.id.hex}
    result = await schema.execute_async(
        query_string, context_value=context, variable_values=variables
    )
    assert result == ExecutionResult(
        data={
            "book": {
                "title": "Dune",
                "author": {"id": Node.encode_id(herbert)},
            }
        }
    )


@pytest.mark.asyncio
async def test_query_node__author(context: Context):
    herbert = context.author_service.one(HERBERT_ID)

    query_string = load_resource("query_node__author.graphql")
    variables = dict(id=Node.encode_id(herbert))
    result = await schema.execute_async(
        query_string, context_value=context, variable_values=variables
    )
    assert result == ExecutionResult(
        data=dict(
            node=dict(
                __typename=Author.__name__,
                id=variables["id"],
                firstName=herbert.first_name,
            )
        )
    )
