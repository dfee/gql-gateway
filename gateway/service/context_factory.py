from flask import request

from gateway.context import ClientRegistry, Context, DataLoaderRegistry
from gateway.dataloader import FunctionalDataLoader
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

        client_registry = ClientRegistry(
            author_client=author_client, book_client=book_client
        )
        data_loader_registry = DataLoaderRegistry(
            author_by_id=FunctionalDataLoader(author_client.batch_load_by_id),
            book_by_id=FunctionalDataLoader(book_client.batch_load_by_id),
            books_by_author_id=FunctionalDataLoader(
                book_client.batch_load_by_author_id
            ),
        )

        return Context(
            clients=client_registry,
            dataloaders=data_loader_registry,
            request=request,
        )

    return _build
