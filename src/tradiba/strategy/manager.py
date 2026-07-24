"""
Strategy manager service.
"""

from __future__ import annotations

from typing import Any

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger

from .base import Strategy
from .bos import BOSStrategy
from .registry import STRATEGY_REGISTRY

logger = get_logger(__name__)

# Basic registry for demonstration
_REGISTRY = {
    "bos_strategy": BOSStrategy
}

from tradiba.strategy.narrative import NarrativeGeneratedEvent  # noqa: E402

class StrategyManager(Service):
    """
    Loads enabled strategies from configuration and manages their lifecycles.
    Routes NarrativeGeneratedEvents to strategies for evaluation.
    """

    def __init__(self, event_bus: EventBus, strategy_configs: dict[str, dict[str, Any]]) -> None:
        self._event_bus = event_bus
        self._configs = strategy_configs
        self._strategies: list[Strategy] = []

    def start(self) -> None:
        """Initialize and start all enabled strategies."""
        logger.info("Starting StrategyManager...")
        for name, config in self._configs.items():
            if not config.get("enabled", False):
                logger.debug("Strategy '%s' is disabled, skipping.", name)
                continue

            if name not in STRATEGY_REGISTRY:
                logger.error("Strategy '%s' is enabled in config but not registered.", name)
                continue

            strategy_cls = STRATEGY_REGISTRY[name]
            try:
                strategy = strategy_cls(name=name, event_bus=self._event_bus, config=config)
                self._strategies.append(strategy)
                logger.info("Loaded strategy '%s'", name)
            except Exception:
                logger.exception("Failed to load strategy '%s'", name)

        # Subscribe to narratives
        self._event_bus.subscribe(NarrativeGeneratedEvent, self.on_narrative)

    def stop(self) -> None:
        """Teardown strategies."""
        logger.info("Stopping StrategyManager...")
        self._event_bus.unsubscribe(NarrativeGeneratedEvent, self.on_narrative)
        self._strategies.clear()

    def on_narrative(self, event: NarrativeGeneratedEvent) -> None:
        """Route narrative to all strategies configured for this symbol/timeframe."""
        for strategy in self._strategies:
            # Strategies should only evaluate narratives for their configured symbol/timeframe
            # if specified in config.
            cfg_symbol = strategy.config.get("symbol")
            cfg_timeframe = strategy.config.get("timeframe")
            
            if cfg_symbol and cfg_symbol != event.narrative.symbol:
                continue
            if cfg_timeframe and cfg_timeframe != event.narrative.timeframe:
                continue
                
            try:
                signals = strategy.evaluate(event.narrative)
                for signal in signals:
                    strategy.publish_signal(signal)
            except Exception:
                logger.exception("Error evaluating strategy '%s'", strategy.name)
