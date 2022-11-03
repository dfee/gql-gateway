from graphql import build_schema

from gateway.generate import get_gen_path
from gateway.util.resource import get_mod_path, load_resource

with open(get_gen_path(), "r") as f:
    schema = build_schema(f.read())
