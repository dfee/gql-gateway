from importlib.util import find_spec

from graphql import build_schema

from gateway.util.graphql import schema_filepath

with open(schema_filepath(), "r") as f:
    schema = build_schema(f.read())
