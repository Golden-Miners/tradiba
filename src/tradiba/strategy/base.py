"""
Strategy base class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from tradiba.events import EventBus

from .events import SignalGeneratedEvent
from .models import Signal


from tradiba.strategy.narrative import MarketNarrative


class Strategy(ABC):
    """
    Base class for all trading strategies.
    
    Strategies evaluate a MarketNarrative and generate trading signals.
    They do not execute trades or manage risk directly.
    """

    def __init__(self, name: str, event_bus: EventBus, config: dict[str, Any]) -> None:
        self.name = name
        self._event_bus = event_bus
        self.config = config

    @abstractmethod
    def evaluate(self, narrative: MarketNarrative) -> list[Signal]:
        """
        Evaluate the current market narrative and return a list of signals.
        If no signals are generated, return an empty list.
        """
        pass

    def publish_signal(self, signal: Signal) -> None:
        """Publish a generated signal to the event bus."""
        from tradiba.logging import get_logger
        get_logger(__name__).info("Strategy generated %s signal for %s", signal.direction.value, signal.symbol)
        self._event_bus.publish(SignalGeneratedEvent(signal=signal))
