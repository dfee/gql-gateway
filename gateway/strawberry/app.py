from flask import Flask, Response
from strawberry.flask.views import GraphQLView

from gateway.context import make_context_factory
from gateway.sql import bootstrap_with_fixtures, make_static_pool_engine

from .schema import schema


class MyGraphQLView(GraphQLView):
    def __init__(self, *args, context_factory, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_factory = context_factory

    def get_context(self, _response: Response):
        return self.context_factory()


def make_app() -> Flask:
    engine = make_static_pool_engine()
    db_context = bootstrap_with_fixtures(engine=engine)
    context_factory = make_context_factory(db_context=db_context)
    app = Flask(__name__)
    app.add_url_rule(
        "/graphql",
        view_func=MyGraphQLView.as_view(
            "graphql_view", context_factory=context_factory, schema=schema
        ),
    )
    return app


def serve(host: str = "0.0.0.0", port: int = 8080):
    app = make_app()
    app.run(host=host, port=port)
