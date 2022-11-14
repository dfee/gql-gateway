from typing import TypeAlias

from strawberry.types import Info as _Info

from gateway.context import Context

Info: TypeAlias = _Info[Context, None]
