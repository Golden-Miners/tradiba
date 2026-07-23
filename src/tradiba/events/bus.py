"""
Production-ready in-process event bus.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from tradiba.logging import get_logger

from .base import Event

logger = get_logger(__name__)

EventHandler = Callable[[Event], None]


class EventBus:
    """
    Publish/subscribe event dispatcher.

    Features:
    - Subscribe
    - Unsubscribe
    - Exception isolation
    - Event statistics
    """

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandler]] = defaultdict(list)
        self._published = 0

    @property
    def published_count(self) -> int:
        return self._published

    def subscribe(
        self,
        event_type: type[Event],
        handler: EventHandler,
    ) -> None:
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: type[Event],
        handler: EventHandler,
    ) -> None:
        handlers = self._handlers.get(event_type)

        if handlers and handler in handlers:
            handlers.remove(handler)

    def publish(
        self,
        event: Event,
    ) -> None:

        self._published += 1

        for handler in list(self._handlers[type(event)]):

            try:
                handler(event)

            except Exception:
                logger.exception(
                    "Unhandled exception in %s",
                    handler.__name__,
                )

    def clear(self) -> None:
        self._handlers.clear()
        self._published = 0