from pathlib import Path

from graphql import GraphQLSchema
from graphql.utilities import lexicographic_sort_schema, print_schema


def gen_schema(schema: GraphQLSchema) -> str:
    return print_schema(lexicographic_sort_schema(schema))


def write_schema(filePath: Path, schema: GraphQLSchema) -> None:
    with open(filePath, encoding="utf-8", mode="w") as f:
        f.write(gen_schema(schema))
