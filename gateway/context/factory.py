from flask import request
from strawberry.flask.views import GraphQLView

from gateway.author import AuthorService
from gateway.book import BookService
from gateway.context import Context
from gateway.dataloaders import DataLoaderRegistry
from gateway.sql.context import DbContext


def make_context_factory(db_context: DbContext):
    def _build():
        session = db_context.sessionmaker()
        author_service = AuthorService(session)
        book_service = BookService(session)

        return Context(
            author_service=author_service,
            book_service=book_service,
            dataloaders=DataLoaderRegistry.setup(
                author_service=author_service, book_service=book_service
            ),
            request=request,
        )

    return _build
