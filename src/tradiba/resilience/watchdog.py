import time
import logging
from tradiba.events import EventBus
from tradiba.events.event import DomainEvent
from tradiba.resilience.configuration import WatchdogConfig
from tradiba.resilience.heartbeat import HeartbeatEvent

logger = logging.getLogger(__name__)

class Watchdog:
    """
    Monitors component heartbeats and escalates failures.
    """
    def __init__(self, config: WatchdogConfig, event_bus: EventBus):
        self.config = config
        self._event_bus = event_bus
        self._last_heartbeats: dict[str, float] = {}
        
        self._event_bus.subscribe(HeartbeatEvent, self._on_heartbeat)

    def _on_heartbeat(self, event: DomainEvent) -> None:
        if isinstance(event, HeartbeatEvent):
            self._last_heartbeats[event.component_name] = time.time()

    def monitor(self) -> list[str]:
        """
        Checks all tracked components. Returns a list of failed components.
        """
        now = time.time()
        failed_components = []
        for component, last_time in self._last_heartbeats.items():
            if now - last_time > (self.config.heartbeat_timeout_seconds * self.config.max_missed_heartbeats):
                failed_components.append(component)
        
        for comp in failed_components:
            self.escalate(comp)
            
        return failed_components

    def escalate(self, component_name: str) -> None:
        """
        Escalation logic for a failed component.
        """
        logger.error(f"Watchdog escalation triggered for component: {component_name}")
        # In a real system, this might trigger a FailoverManager or restart sequence.
