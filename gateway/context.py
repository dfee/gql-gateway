from dataclasses import dataclass
from functools import wraps
from typing import Any, TypeGuard

from gateway.author import AuthorService
from gateway.book import BookService
from gateway.graphene.dataloaders import DataLoaderRegistry


@dataclass
class Context:
    dataloaders: DataLoaderRegistry
    author_service: AuthorService
    book_service: BookService


def is_context(val: Any) -> TypeGuard[Context]:
    return isinstance(val, Context)


def as_context(val: Any) -> Context:
    if is_context(val):
        return val
    raise ValueError("Invalid context")


def with_context(f):
    @wraps(f)
    def wrapper(root, info, **kwargs):
        return f(root, info, as_context(info.context), **kwargs)

    return wrapper
