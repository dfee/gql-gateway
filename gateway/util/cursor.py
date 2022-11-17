from typing import Any, Callable, TypeVar

T = TypeVar("T")


def take_first(default: T, *values: T) -> T:
    return next(_value for _value in [*values, default] if _value is not None)


def make_limiter(default: int, ceiling: int) -> Callable[..., int]:
    def _limiter(*values: int) -> int:
        return min(ceiling, take_first(default, *values))

    return _limiter
