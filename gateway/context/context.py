import typing
from dataclasses import dataclass
from functools import wraps

from flask import Request

from gateway.client.author import AbstractAuthorClient
from gateway.client.book import AbstractBookClient
from gateway.dataloaders import DataLoaderRegistry


@dataclass
class Context:
    author_client: AbstractAuthorClient
    book_client: AbstractBookClient
    dataloaders: DataLoaderRegistry
    request: typing.Optional[Request]


def is_context(val: typing.Any) -> typing.TypeGuard[Context]:
    return isinstance(val, Context)


def as_context(val: typing.Any) -> Context:
    if is_context(val):
        return val
    raise ValueError("Invalid context")


def with_context(f):
    @wraps(f)
    def wrapper(root, info, *args, **kwargs):
        return f(root, info, as_context(info.context), *args, **kwargs)

    return wrapper
