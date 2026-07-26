from enum import Enum
from typing import Any
from uuid import UUID

class StorageZone(Enum):
    RAW = "raw"
    VALIDATED = "validated"
    CURATED = "curated"
    FEATURE_STORE = "feature_store"
    ARCHIVE = "archive"

class DataLakehouse:
    """Manages the lifecycle and location of datasets across storage zones."""
    def __init__(self) -> None:
        self._zone_inventory: dict[StorageZone, list[UUID]] = {
            zone: [] for zone in StorageZone
        }

    def write_to_zone(self, zone: StorageZone, dataset_id: UUID, data: list[dict[str, Any]]) -> None:
        """Mock implementation to register data in a specific zone."""
        if dataset_id not in self._zone_inventory[zone]:
            self._zone_inventory[zone].append(dataset_id)
            
    def get_zone_inventory(self, zone: StorageZone) -> list[UUID]:
        return self._zone_inventory[zone]
