from dataclasses import dataclass
from uuid import UUID

@dataclass
class DatasetMetadata:
    source: str
    refresh_frequency: str
    quality_score: float
    permissions: list[str]
    tags: list[str]

class MetadataService:
    """Tracks extended metadata associated with datasets."""
    def __init__(self) -> None:
        self._metadata: dict[UUID, DatasetMetadata] = {}

    def update_metadata(self, dataset_id: UUID, metadata: DatasetMetadata) -> None:
        self._metadata[dataset_id] = metadata

    def get_metadata(self, dataset_id: UUID) -> DatasetMetadata | None:
        return self._metadata.get(dataset_id)
