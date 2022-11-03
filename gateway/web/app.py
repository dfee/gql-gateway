from flask import Flask
from graphql_server.flask import GraphQLView

from gateway.author import AuthorService
from gateway.book import BookService
from gateway.context import Context
from gateway.graphene.dataloaders import DataLoaderRegistry
from gateway.sql.context import DbContext, bootstrap, make_static_pool_engine
from gateway.sql.fixtures import load_fixtures


def setup_db() -> DbContext:
    db_context = bootstrap(engine=make_static_pool_engine())
    with db_context.sessionmaker() as session:
        load_fixtures(session)
        session.commit()
    return db_context


def context_factory(db_context: DbContext):
    def _build():
        session = db_context.sessionmaker()
        author_service = AuthorService(session)
        book_service = BookService(session)

        return Context(
            dataloaders=DataLoaderRegistry.setup(
                author_service=author_service, book_service=book_service
            ),
            author_service=author_service,
            book_service=book_service,
        )

    return _build


# TODO: really need to use context_manager here...
# probably on Flask's `g`
factory = context_factory(db_context=setup_db())


class CustomGraphQLView(GraphQLView):
    def get_context(self):
        return factory()


def serve_graphene():
    from gateway.graphene.schema import schema

    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        view_func=CustomGraphQLView.as_view(
            "graphql",
            batch=True,
            graphiql=True,
            schema=schema.graphql_schema,
        ),
    )

    app.run(host="0.0.0.0", port=8080)


def serve_core():
    from gateway.core.schema import schema

    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        view_func=CustomGraphQLView.as_view(
            "graphql",
            batch=True,
            graphiql=True,
            schema=schema,
        ),
    )

    app.run(host="0.0.0.0", port=8080)
