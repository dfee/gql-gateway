from pathlib import Path
from gateway.graphene.schema import schema
from gateway.util.resource import get_mod_path
from gateway.util.graphql import write_schema


def get_gen_path() -> Path:
    return get_mod_path(__file__).joinpath("schema.generated.graphql")


def gen_schema() -> None:
    write_schema(get_gen_path(), schema.graphql_schema)
