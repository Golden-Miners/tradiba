"""
Base event types.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


from tradiba.ports.clock import get_clock


@dataclass(slots=True, frozen=True, kw_only=True)
class Event:
    """
    Base class for all events.
    """

    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: get_clock().now())