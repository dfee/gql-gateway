from flask import request

from gateway.client.author.client import AuthorClient
from gateway.client.book.client import BookClient
from gateway.context import Context
from gateway.dataloaders import DataLoaderRegistry
from gateway.service.author import AuthorService
from gateway.service.book import BookService
from gateway.sql.context import DbContext


def make_context_factory(db_context: DbContext):
    def _build():
        session = db_context.sessionmaker()
        author_service = AuthorService(session)
        author_client = AuthorClient(author_service=author_service)
        book_service = BookService(session)
        book_client = BookClient(book_service=book_service)

        return Context(
            author_client=author_client,
            book_client=book_client,
            dataloaders=DataLoaderRegistry.setup(
                author_client=author_client, book_client=book_client
            ),
            request=request,
        )

    return _build
