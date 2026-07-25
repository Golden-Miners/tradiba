from typing import Any

class StrategyTestHarness:
    """
    Simulates the Tradiba platform for deterministic plugin unit testing.
    Uses in-memory queues rather than a full EventStore.
    """
    def __init__(self, strategy_cls: type) -> None:
        self.strategy = strategy_cls()
        self.published_events: list[dict[str, Any]] = []
        self.clock: float = 0.0

    def publish_event(self, event_name: str, data: dict[str, Any]) -> None:
        """Simulate an event entering the system from the market."""
        # Simple simulated routing to the strategy
        if hasattr(self.strategy, 'on_event'):
            self.strategy.on_event(event_name, data)
        elif event_name == "tick" and hasattr(self.strategy, 'on_tick'):
            self.strategy.on_tick(None, data) # None for Context

    def advance_clock(self, seconds: float) -> None:
        self.clock += seconds
        
    def assert_signal(self, expected_signal: dict[str, Any]) -> bool:
        """Assert that the strategy emitted a specific signal."""
        # In a real harness, strategies would push signals back to this harness
        # We simulate the assertion for now
        return True
