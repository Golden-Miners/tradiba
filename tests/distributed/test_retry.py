import pytest
from tradiba.distributed.exceptions import RetryableError, FatalError
import asyncio

async def retry_with_backoff(func, max_retries=3):
    """Simple retry loop for testing"""
    for attempt in range(max_retries):
        try:
            return await func()
        except RetryableError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(0.01)

@pytest.mark.asyncio
async def test_retry_success_after_failure():
    attempts = 0
    
    async def flappy_func():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RetryableError("Network timeout")
        return "success"
        
    result = await retry_with_backoff(flappy_func)
    assert result == "success"
    assert attempts == 3

@pytest.mark.asyncio
async def test_fatal_error_no_retry():
    attempts = 0
    
    async def fatal_func():
        nonlocal attempts
        attempts += 1
        raise FatalError("Bad config")
        
    with pytest.raises(FatalError):
        await retry_with_backoff(fatal_func)
        
    assert attempts == 1
