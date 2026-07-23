"""
Event handler definitions.
"""

from __future__ import annotations

from collections.abc import Callable

from .base import Event

EventHandler = Callable[[Event], None]