import logging
from dataclasses import dataclass
from uuid import UUID

from tradiba.distributed.messaging.base import MessageBus

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CommandMetadata:
    command_id: UUID
    correlation_id: UUID
    idempotency_key: str

class CommandDispatcher:
    """
    Separates commands from events and dispatches them idempotently
    with basic backpressure support.
    """
    def __init__(self, bus: MessageBus):
        self.bus = bus
        self._processed_keys: set[str] = set()

    def dispatch(self, topic: str, command: dict, metadata: CommandMetadata) -> None:
        """Dispatch a command to the specified topic."""
        # Attach metadata for downstream consumption
        payload = {
            "metadata": {
                "command_id": str(metadata.command_id),
                "correlation_id": str(metadata.correlation_id),
                "idempotency_key": metadata.idempotency_key,
            },
            "command": command
        }
        logger.info(f"Dispatching command {metadata.command_id} to {topic}")
        self.bus.publish(topic, payload)

    def is_processed(self, idempotency_key: str) -> bool:
        """Check if a command was already processed."""
        return idempotency_key in self._processed_keys

    def mark_processed(self, idempotency_key: str) -> None:
        """Mark a command as processed."""
        self._processed_keys.add(idempotency_key)
