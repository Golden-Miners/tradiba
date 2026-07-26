from uuid import UUID
from enum import Enum

class StorageTier(Enum):
    ACTIVE = "active"
    WARM = "warm"
    COLD = "cold"
    ARCHIVE = "archive"

class ArchivalService:
    """Migrates data between storage tiers based on lifecycle events."""
    def __init__(self) -> None:
        self._data_tiers: dict[UUID, StorageTier] = {}

    def migrate(self, dataset_id: UUID, target_tier: StorageTier) -> None:
        self._data_tiers[dataset_id] = target_tier
        
    def get_tier(self, dataset_id: UUID) -> StorageTier:
        return self._data_tiers.get(dataset_id, StorageTier.ACTIVE)
