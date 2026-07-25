from tradiba.events import EventBus
from tradiba.resilience.events import FailoverActivatedEvent
import logging

logger = logging.getLogger(__name__)

class FailoverManager:
    """
    Manages promotion and rollback of secondary systems upon primary failure.
    """
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus
        self._active_secondaries: set[str] = set()

    def promote_secondary(self, component_name: str, secondary_target: str) -> None:
        """
        Activates a secondary component/service to take over from a failed primary.
        """
        logger.warning(f"Promoting secondary '{secondary_target}' for component '{component_name}'")
        self._active_secondaries.add(component_name)
        
        self._event_bus.publish(
            FailoverActivatedEvent(
                component_name=component_name,
                secondary_target=secondary_target
            )
        )

    def rollback(self, component_name: str) -> None:
        """
        Reverts back to the primary component once it is healthy.
        """
        if component_name in self._active_secondaries:
            logger.info(f"Rolling back to primary for component '{component_name}'")
            self._active_secondaries.remove(component_name)
            # In reality, this might trigger another event or API call
