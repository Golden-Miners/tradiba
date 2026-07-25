import time
from dataclasses import dataclass
from tradiba.events import EventBus
from tradiba.events.event import DomainEvent
import threading

@dataclass(frozen=True)
class HeartbeatEvent(DomainEvent):
    component_name: str

class HeartbeatEmitter:
    """
    Emits regular heartbeats to the event bus.
    """
    def __init__(self, component_name: str, event_bus: EventBus, interval_seconds: float = 5.0):
        self.component_name = component_name
        self._event_bus = event_bus
        self.interval_seconds = interval_seconds
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name=f"Heartbeat-{self.component_name}")
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()

    def _run_loop(self) -> None:
        while self._running:
            self._event_bus.publish(HeartbeatEvent(component_name=self.component_name))
            time.sleep(self.interval_seconds)
