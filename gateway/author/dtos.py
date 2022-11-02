from dataclasses import dataclass
from uuid import UUID
from typing import List


@dataclass
class AuthorDto:
    id: UUID
    first_name: str
    last_name: str
    book_ids: List[UUID]
