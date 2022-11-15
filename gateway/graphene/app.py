from flask import Flask
from graphql_server.flask import GraphQLView

from gateway.repository import bootstrap_with_fixtures, make_static_pool_engine
from gateway.service.context_factory import make_context_factory

from .schema import schema


def make_app() -> Flask:
    engine = make_static_pool_engine()
    db_context = bootstrap_with_fixtures(engine=engine)
    context_factory = make_context_factory(db_context=db_context)
    app = Flask(__name__)
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            batch=True,
            get_context=context_factory,
            graphiql=True,
            schema=schema.graphql_schema,
        ),
    )
    return app


def serve(host: str = "0.0.0.0", port: int = 8080):
    app = make_app()
    app.run(host=host, port=port)
