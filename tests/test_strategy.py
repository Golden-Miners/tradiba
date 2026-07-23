"""
Tests for the Strategy Manager.
"""

from __future__ import annotations

from typing import Any

from tradiba.events import EventBus
from tradiba.strategy import (
    Strategy,
    StrategyManager,
    register_strategy,
)


@register_strategy("dummy_ok")
class DummyOkStrategy(Strategy):
    def __init__(self, name: str, event_bus: EventBus, config: dict[str, Any]) -> None:
        super().__init__(name, event_bus, config)
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


@register_strategy("dummy_fail_start")
class DummyFailStartStrategy(Strategy):
    def start(self) -> None:
        raise RuntimeError("Failed to start")

    def stop(self) -> None:
        pass


@register_strategy("dummy_fail_stop")
class DummyFailStopStrategy(Strategy):
    def start(self) -> None:
        pass

    def stop(self) -> None:
        raise RuntimeError("Failed to stop")


class TestStrategyManager:
    def test_loads_enabled_strategies(self):
        bus = EventBus()
        configs = {
            "dummy_ok": {"enabled": True},
            "dummy_fail_start": {"enabled": False},  # disabled
            "non_existent": {"enabled": True},  # doesn't exist in registry
        }

        manager = StrategyManager(bus, configs)
        manager.start()

        assert len(manager._strategies) == 1
        strategy = manager._strategies[0]
        assert isinstance(strategy, DummyOkStrategy)
        assert strategy.started is True

        manager.stop()
        assert strategy.stopped is True
        assert len(manager._strategies) == 0

    def test_handles_start_exception(self):
        bus = EventBus()
        configs = {
            "dummy_fail_start": {"enabled": True},
            "dummy_ok": {"enabled": True},
        }

        manager = StrategyManager(bus, configs)
        manager.start()  # Should not raise

        # dummy_ok should still have started successfully
        assert len(manager._strategies) == 1
        assert isinstance(manager._strategies[0], DummyOkStrategy)

    def test_handles_stop_exception(self):
        bus = EventBus()
        configs = {
            "dummy_fail_stop": {"enabled": True},
            "dummy_ok": {"enabled": True},
        }

        manager = StrategyManager(bus, configs)
        manager.start()
        
        assert len(manager._strategies) == 2

        manager.stop()  # Should not raise

        # The list should be cleared
        assert len(manager._strategies) == 0
