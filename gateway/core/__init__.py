from graphql import build_schema
from gateway.util.resource import load_resource
from gateway.generate import get_gen_path

with open(get_gen_path(), "r") as f:
    schema = build_schema(f.read())
