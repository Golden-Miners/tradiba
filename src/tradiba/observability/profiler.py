import time
from contextlib import contextmanager
from typing import Generator

from .metrics import (
    strategy_latency_seconds,
    execution_latency_seconds,
    market_structure_latency_seconds
)


class Profiler:
    """Helper to collect latency metrics for pipeline stages."""

    @staticmethod
    @contextmanager
    def measure_strategy() -> Generator[None, None, None]:
        start = time.perf_counter()
        try:
            yield
        finally:
            strategy_latency_seconds.observe(time.perf_counter() - start)

    @staticmethod
    @contextmanager
    def measure_execution() -> Generator[None, None, None]:
        start = time.perf_counter()
        try:
            yield
        finally:
            execution_latency_seconds.observe(time.perf_counter() - start)

    @staticmethod
    @contextmanager
    def measure_market_structure() -> Generator[None, None, None]:
        start = time.perf_counter()
        try:
            yield
        finally:
            market_structure_latency_seconds.observe(time.perf_counter() - start)
