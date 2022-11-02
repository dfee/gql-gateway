from aiohttp import web
from .app import core_app, graphene_app


def serve_core():
    web.run_app(core_app())


def serve_graphene():
    web.run_app(graphene_app())
