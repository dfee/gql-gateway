import pytest
from graphene import Schema as GrapheneSchema
from graphql import GraphQLSchema, graphql_sync
from strawberry import Schema as StrawberrySchema

from gateway.core.schema import make_schema as _make_core_schema
from gateway.graphene.schema import schema as _graphene_schema
from gateway.strawberry.schema import schema as _strawberry_schema


@pytest.fixture
def core_schema() -> GraphQLSchema:
    return _make_core_schema()


@pytest.fixture
def graphene_schema() -> GrapheneSchema:
    yield _graphene_schema


@pytest.fixture
def strawberry_schema() -> StrawberrySchema:
    yield _strawberry_schema


@pytest.fixture
def graphene_native_schema(graphene_schema: GrapheneSchema) -> GraphQLSchema:
    return graphene_schema.graphql_schema


@pytest.fixture
def strawberry_native_schema(strawberry_schema: StrawberrySchema) -> GraphQLSchema:
    return strawberry_schema._schema


@pytest.fixture(
    params=["core_schema", "graphene_native_schema", "strawberry_native_schema"]
)
def native_schema(request: pytest.FixtureRequest):
    yield request.getfixturevalue(request.param)


@pytest.fixture
def core_execute_sync(core_schema: GraphQLSchema):
    def _execute_sync(source: str, **kwargs):
        return graphql_sync(core_schema, source, **kwargs)

    return _execute_sync


@pytest.fixture
def graphene_execute_sync(graphene_schema: GrapheneSchema):
    def _execute_sync(source, **kwargs):
        return graphene_schema.execute(source, **kwargs)

    return _execute_sync


@pytest.fixture
def strawberry_execute_sync(strawberry_schema: StrawberrySchema):
    def _execute_sync(source, **kwargs):
        return strawberry_schema.execute_sync(source, **kwargs)

    return _execute_sync


@pytest.fixture(
    params=["core_execute_sync", "graphene_execute_sync", "strawberry_execute_sync"]
)
def execute_sync(request: pytest.FixtureRequest):
    yield request.getfixturevalue(request.param)
