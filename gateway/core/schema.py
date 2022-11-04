from graphql import GraphQLSchema, build_schema

from gateway.util.graphql import schema_filepath

from .resolvers import bind_resolvers


def make_schema() -> GraphQLSchema:
    with open(schema_filepath(), "r") as f:
        schema = build_schema(f.read())

    bind_resolvers(schema)
    return schema
