from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


@dataclass
class DbContext:
    engine: Engine
    sessionmaker: sessionmaker
