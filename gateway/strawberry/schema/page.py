from enum import Enum
from typing import Optional

import strawberry

from gateway.client.page import PageInfo as PageInfoDto
from gateway.client.page import SortOrder as SortOrderDto

__all__ = [
    "PageInfo",
    "SortOrder",
]


@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]

    def to_dto(self) -> PageInfoDto:
        return PageInfoDto(
            end_cursor=self.end_cursor,
            has_next_page=self.has_next_page,
            has_previous_page=self.has_previous_page,
            start_cursor=self.start_cursor,
        )

    @classmethod
    def from_dto(cls: "PageInfo", dto: PageInfoDto) -> "PageInfo":
        return cls(
            end_cursor=dto.end_cursor,
            has_next_page=dto.has_next_page,
            has_previous_page=dto.has_previous_page,
            start_cursor=dto.start_cursor,
        )


@strawberry.enum
class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"

    def to_dto(self) -> SortOrderDto:
        return SortOrderDto(self.value)

    @classmethod
    def from_dto(cls: "SortOrder", dto: SortOrderDto) -> "SortOrder":
        return cls(dto.value)
