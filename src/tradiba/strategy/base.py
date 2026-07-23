"""
Strategy base class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from tradiba.events import EventBus

from .events import SignalGeneratedEvent
from .models import Signal


class Strategy(ABC):
    """
    Base class for all trading strategies.
    
    Strategies are responsible for analyzing market events and generating
    trading signals. They do not execute trades or manage risk directly.
    """

    def __init__(self, name: str, event_bus: EventBus, config: dict[str, Any]) -> None:
        self.name = name
        self._event_bus = event_bus
        self.config = config

    @abstractmethod
    def start(self) -> None:
        """
        Initialize the strategy.
        This is where the strategy should subscribe to required events on the event bus.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Teardown the strategy.
        This is where the strategy should unsubscribe from events and clean up state.
        """
        pass

    def publish_signal(self, signal: Signal) -> None:
        """Publish a generated signal to the event bus."""
        self._event_bus.publish(SignalGeneratedEvent(signal=signal))
