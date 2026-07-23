"""
Strategy registry for dynamic loading.
"""

from __future__ import annotations

from .base import Strategy

STRATEGY_REGISTRY: dict[str, type[Strategy]] = {}


def register_strategy(name: str):
    """Decorator to register a strategy class under a specific name."""

    def decorator(cls: type[Strategy]) -> type[Strategy]:
        STRATEGY_REGISTRY[name] = cls
        return cls

    return decorator
