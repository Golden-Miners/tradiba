"""
Scheduled task definitions.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(slots=True)
class Task:
    """
    Represents a scheduled task.
    """

    name: str
    interval: float
    action: Callable[[], None]

    elapsed: float = 0.0
    enabled: bool = True
    running: bool = field(default=False, init=False)