from graphql import build_schema
from gateway.util.resource import load_resource

schema = build_schema(load_resource(__name__, "schema.graphql"))
