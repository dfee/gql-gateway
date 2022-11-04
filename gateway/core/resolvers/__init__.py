from graphql import GraphQLSchema

from .author import Author
from .book import Book
from .node import Node
from .query import Query


def bind_resolvers(schema: GraphQLSchema) -> None:
    for resolver in [Author, Book, Node, Query]:
        resolver.bind(schema)
