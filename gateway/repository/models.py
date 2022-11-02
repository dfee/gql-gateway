from dataclasses import dataclass
from uuid import UUID
from typing import List


@dataclass
class Author:
    id: UUID
    first_name: str
    last_name: str
    book_ids: List[UUID]


@dataclass
class Book:
    id: UUID
    title: str
    author_id: UUID
