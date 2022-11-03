from dataclasses import dataclass

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, StaticPool

from .models import Base


@dataclass
class DbContext:
    engine: Engine
    sessionmaker: sessionmaker


def make_default_engine():
    return create_engine("sqlite://")


def make_static_pool_engine():
    return create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )


def bootstrap(engine: Engine) -> DbContext:
    Base.metadata.create_all(engine)
    return DbContext(engine=engine, sessionmaker=sessionmaker(bind=engine))
