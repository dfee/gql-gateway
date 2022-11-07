from flask import Flask, request
from graphql_server.flask import GraphQLView

from gateway.author import AuthorService
from gateway.book import BookService
from gateway.context import Context
from gateway.dataloaders import DataLoaderRegistry
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
            author_service=author_service,
            book_service=book_service,
            dataloaders=DataLoaderRegistry.setup(
                author_service=author_service, book_service=book_service
            ),
            request=request,
        )

    return _build


# TODO: really need to use context_manager here...
# probably on Flask's `g`
db_context = setup_db()
factory = context_factory(db_context)


def serve_graphene():
    from gateway.graphene.schema import schema

    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        # view_func=CustomGraphQLView.as_view(
        view_func=GraphQLView.as_view(
            "graphql",
            batch=True,
            get_context=factory,
            graphiql=True,
            schema=schema.graphql_schema,
        ),
    )

    app.run(host="0.0.0.0", port=8080)


def serve_core():
    from gateway.core.schema import make_schema

    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            batch=True,
            get_context=factory,
            graphiql=True,
            schema=make_schema(),
        ),
    )

    app.run(host="0.0.0.0", port=8080)
