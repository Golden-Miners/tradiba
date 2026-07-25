from tradiba.dev.testing import StrategyTestHarness
from typing import Any

class MockStrategy:
    def __init__(self):
        self.received_events: list[tuple[str, dict[str, Any]]] = []
        
    def on_event(self, name: str, data: dict[str, Any]) -> None:
        self.received_events.append((name, data))
        
    def on_tick(self, ctx: Any, data: Any) -> None:
        pass

def test_harness_routing():
    harness = StrategyTestHarness(MockStrategy)
    
    harness.publish_event("trade", {"price": 100})
    
    assert len(harness.strategy.received_events) == 1
    assert harness.strategy.received_events[0] == ("trade", {"price": 100})
    
    harness.advance_clock(10.0)
    assert harness.clock == 10.0
    
    assert harness.assert_signal({})
