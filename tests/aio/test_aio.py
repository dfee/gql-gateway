import asyncio

import pytest


async def sleep_msg(duration: int, message: str) -> str:
    await asyncio.sleep(duration)
    return message


@pytest.mark.asyncio
async def test_sleep():
    msg = "hello world"
    rv = await sleep_msg(0.1, msg)
    assert rv == msg
