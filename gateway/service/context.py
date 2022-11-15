from flask import request

from gateway.context import Context
from gateway.dataloader import DataLoaderRegistry
from gateway.repository.context import DbContext
from gateway.service.author import AuthorService
from gateway.service.author.client import NativeAuthorClient
from gateway.service.book import BookService
from gateway.service.book.client import NativeBookClient


def make_context_factory(db_context: DbContext):
    def _build():
        session = db_context.sessionmaker()
        author_service = AuthorService(session)
        author_client = NativeAuthorClient(author_service=author_service)
        book_service = BookService(session)
        book_client = NativeBookClient(book_service=book_service)

        return Context(
            author_client=author_client,
            book_client=book_client,
            dataloaders=DataLoaderRegistry.setup(
                author_client=author_client, book_client=book_client
            ),
            request=request,
        )

    return _build
