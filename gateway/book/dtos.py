from dataclasses import dataclass
from uuid import UUID


@dataclass
class BookDto:
    id: UUID
    title: str
    author_id: UUID
