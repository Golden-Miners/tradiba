"""
Strategy manager service.
"""

from __future__ import annotations

from typing import Any

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger

from .base import Strategy
from .registry import STRATEGY_REGISTRY

logger = get_logger(__name__)


class StrategyManager(Service):
    """
    Loads enabled strategies from configuration and manages their lifecycles.
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
                strategy.start()
                self._strategies.append(strategy)
                logger.info("Started strategy '%s'", name)
            except Exception:
                logger.exception("Failed to start strategy '%s'", name)

    def stop(self) -> None:
        """Stop all running strategies."""
        logger.info("Stopping StrategyManager...")
        for strategy in self._strategies:
            try:
                strategy.stop()
                logger.info("Stopped strategy '%s'", strategy.name)
            except Exception:
                logger.exception("Failed to stop strategy '%s'", strategy.name)
        
        self._strategies.clear()
