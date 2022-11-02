from aiohttp import web
from graphql_server.aiohttp import GraphQLView


def core_app():
    from gateway.core import schema

    app = web.Application()
    GraphQLView.attach(
        app, schema=schema, batch=True, route_path="/graphql", graphiql=True
    )
    return app


def graphene_app():
    from gateway.graphene.schema import schema

    app = web.Application()
    GraphQLView.attach(
        app, schema=schema, batch=True, route_path="/graphql", graphiql=True
    )
    return app
