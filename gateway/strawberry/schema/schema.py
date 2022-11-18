import strawberry

from .query import Query

__all__ = [
    "make_schema",
]


def make_schema():
    return strawberry.Schema(query=Query)
