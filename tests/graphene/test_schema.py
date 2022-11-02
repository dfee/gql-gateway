from graphql import ExecutionResult
from gateway.graphene.schema import schema
from gateway.repository.models import Node, Author
from gateway.repository import HERBERT_ID, DUNE_ID, author_repository, book_repository

from tests.utils import load_resource as _load_resource

load_resource = lambda resource: _load_resource(__name__, resource)


def test_query_author():
    query_string = load_resource("query_author.graphql")
    variables = {"id": HERBERT_ID.hex}
    result = schema.execute(query_string, variable_values=variables)
    assert result == ExecutionResult(
        data={
            "author": {
                "firstName": "Frank",
                "books": [{"id": book_repository.get_or_throw(DUNE_ID)._node_id}],
            }
        }
    )


def test_query_book():
    query_string = load_resource("query_book.graphql")
    variables = {"id": DUNE_ID.hex}
    result = schema.execute(query_string, variable_values=variables)
    assert result == ExecutionResult(
        data={
            "book": {
                "title": "Dune",
                "author": {"id": author_repository.get_or_throw(HERBERT_ID)._node_id},
            }
        }
    )


def test_query_node__author():
    query_string = "query AuthorByNode($id: ID!) { node(id: $id) { __typename id ...on Author { firstName } } }"
    variables = dict(id=author_repository.get_or_throw(HERBERT_ID)._node_id)
    result = schema.execute(query_string, variable_values=variables)
    assert result == ExecutionResult(
        data=dict(
            node=dict(
                __typename=Author._typename,
                id=variables["id"],
                firstName="Frank",
            )
        )
    )
