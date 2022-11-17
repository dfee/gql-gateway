import pytest

from gateway.util.cursor import make_limiter


@pytest.mark.parametrize(
    "default,limit,values,expected",
    [
        [5, 10, [1], 1],
        [5, 10, [None, 1], 1],
        [5, 10, [], 5],
        [5, 10, [100], 10],
    ],
)
def test_limiter(default, limit, values, expected):
    limiter = make_limiter(default, limit)
    assert limiter(*values) == expected
