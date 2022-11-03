from aiohttp import web
from graphql_server.aiohttp import GraphQLView


def aiohttp_core_app():
    from gateway.core import schema

    app = web.Application()
    GraphQLView.attach(
        app, schema=schema, batch=True, route_path="/graphql", graphiql=True
    )
    return app


def serve_aiohttp_core():
    web.run_app(aiohttp_core_app())


def aiohttp_graphene_app():
    from gateway.graphene.schema import schema

    app = web.Application()
    GraphQLView.attach(
        app, schema=schema, batch=True, route_path="/graphql", graphiql=True
    )
    return app


def serve_aiohttp_graphene():
    web.run_app(aiohttp_graphene_app())
