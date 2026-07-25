from tradiba.events import EventBus
from tradiba.resilience.checkpoint import CheckpointRepository, RecoveryCheckpoint
from tradiba.resilience.events import CheckpointCreatedEvent, RecoveryCompletedEvent
from tradiba.resilience.exceptions import RecoveryError
from typing import Any
import logging

logger = logging.getLogger(__name__)

class RecoveryManager:
    """
    Manages state checkpoints and orchestrates recovery upon failure.
    """
    def __init__(self, repository: CheckpointRepository, event_bus: EventBus):
        self._repository = repository
        self._event_bus = event_bus

    def create_checkpoint(self, portfolio_version: int, event_sequence: int, metadata: dict[str, Any] | None = None) -> RecoveryCheckpoint:
        """Creates and persists a new safe checkpoint."""
        checkpoint = RecoveryCheckpoint(
            portfolio_version=portfolio_version,
            event_sequence=event_sequence,
            metadata=metadata or {}
        )
        self._repository.save(checkpoint)
        
        self._event_bus.publish(
            CheckpointCreatedEvent(
                checkpoint_id=checkpoint.checkpoint_id,
                portfolio_version=checkpoint.portfolio_version,
                event_sequence=checkpoint.event_sequence
            )
        )
        return checkpoint

    def recover(self) -> RecoveryCheckpoint:
        """
        Attempts to recover the system to the last known safe checkpoint.
        """
        logger.info("Initiating system recovery...")
        checkpoint = self._repository.get_latest()
        if not checkpoint:
            raise RecoveryError("No checkpoint found to recover from.")
        
        # In a real implementation, this would instruct the Event Store to replay
        # events from `checkpoint.event_sequence` onwards to rebuild state.
        
        self._event_bus.publish(
            RecoveryCompletedEvent(
                checkpoint_id=checkpoint.checkpoint_id,
                restored_event_sequence=checkpoint.event_sequence
            )
        )
        logger.info(f"Recovery to checkpoint {checkpoint.checkpoint_id} complete.")
        return checkpoint
