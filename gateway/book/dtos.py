from dataclasses import dataclass
from typing import Optional


@dataclass
class BookDto:
    id: int
    title: str
    author_id: int


@dataclass
class CreateBookDto:
    title: str
    author_id: int
    id: Optional[int] = None
