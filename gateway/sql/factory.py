from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .context import DbContext
from .fixtures import load_fixtures
from .models import Base


def make_default_engine():
    return create_engine("sqlite://")


def make_static_pool_engine():
    return create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )


def bootstrap(engine: Engine) -> DbContext:
    Base.metadata.create_all(engine)
    return DbContext(engine=engine, sessionmaker=sessionmaker(bind=engine))


def bootstrap_with_fixtures(engine: Engine) -> DbContext:
    db_context = bootstrap(engine=engine)
    with db_context.sessionmaker() as session:
        load_fixtures(session)
        session.commit()
    return db_context
