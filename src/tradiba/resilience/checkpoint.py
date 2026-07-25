from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class RecoveryCheckpoint:
    """
    Immutable representation of a confirmed system state.
    """
    checkpoint_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    portfolio_version: int = 0
    event_sequence: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

class CheckpointRepository:
    """
    Interface for saving and retrieving checkpoints.
    """
    def save(self, checkpoint: RecoveryCheckpoint) -> None:
        raise NotImplementedError

    def get_latest(self) -> RecoveryCheckpoint | None:
        raise NotImplementedError

class InMemoryCheckpointRepository(CheckpointRepository):
    def __init__(self) -> None:
        self._checkpoints: list[RecoveryCheckpoint] = []

    def save(self, checkpoint: RecoveryCheckpoint) -> None:
        self._checkpoints.append(checkpoint)

    def get_latest(self) -> RecoveryCheckpoint | None:
        if not self._checkpoints:
            return None
        # Assuming they are saved in order
        return self._checkpoints[-1]
