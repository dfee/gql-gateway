from graphene import Schema

from .query import Query

__all__ = ["make_schema"]


def make_schema():
    return Schema(query=Query)
