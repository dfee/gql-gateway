from importlib.util import find_spec
from pathlib import Path

from graphql import GraphQLSchema
from graphql.utilities import lexicographic_sort_schema, print_schema

PACKAGE_NAME = "gateway"
SCHEMA_FILENAME = "schema.graphql"


def pprint_schema(schema: GraphQLSchema) -> str:
    return print_schema(lexicographic_sort_schema(schema))


def schema_dirpath() -> Path:
    return Path(find_spec(PACKAGE_NAME).origin).parent


def schema_filepath() -> Path:
    return schema_dirpath().joinpath(SCHEMA_FILENAME)
