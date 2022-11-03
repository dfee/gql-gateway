from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthorDto:
    id: int
    first_name: str
    last_name: str


@dataclass
class CreateAuthorDto:
    first_name: str
    last_name: str
    id: Optional[int] = None
