import time
import threading
from tradiba.resilience.configuration import RateLimiterConfig
from tradiba.resilience.exceptions import RateLimitExceededError

class RateLimiter:
    """
    Token bucket rate limiter to protect external services.
    """
    def __init__(self, config: RateLimiterConfig):
        self.config = config
        self._tokens = config.max_requests
        self._last_refill_time = time.time()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self._last_refill_time
        
        # Calculate tokens to add based on elapsed time
        tokens_to_add = int(elapsed * (self.config.max_requests / self.config.time_window_seconds))
        
        if tokens_to_add > 0:
            self._tokens = min(self.config.max_requests, self._tokens + tokens_to_add)
            self._last_refill_time = now

    def acquire(self, tokens: int = 1) -> None:
        """
        Attempts to acquire tokens. Raises RateLimitExceededError if limit is reached.
        """
        with self._lock:
            self._refill()
            if self._tokens < tokens:
                raise RateLimitExceededError("Rate limit exceeded.")
            self._tokens -= tokens
