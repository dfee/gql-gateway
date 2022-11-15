import typing
from dataclasses import dataclass
from functools import wraps

from flask import Request

from gateway.client.author import AuthorClient, AuthorDto
from gateway.client.book import BookClient, BookDto
from gateway.dataloader import DataLoader


@dataclass
class ClientRegistry:
    author_client: AuthorClient
    book_client: BookClient


@dataclass
class DataLoaderRegistry:
    author_by_id: DataLoader[int, AuthorDto]
    book_by_id: DataLoader[int, BookDto]
    books_by_author_id: DataLoader[int, typing.List[BookDto]]


@dataclass
class Context:
    clients: ClientRegistry
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
