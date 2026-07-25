from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class Dataset:
    """
    Immutable, reproducible dataset definition.
    All research starts with datasets.
    """
    dataset_id: UUID
    symbol: str
    timeframe: str
    start: datetime
    end: datetime
    feature_version: str
    label_version: str

class DatasetRegistry:
    """Registry to load and store dataset metadata."""
    def __init__(self):
        self._datasets: dict[UUID, Dataset] = {}

    def register(self, dataset: Dataset) -> None:
        self._datasets[dataset.dataset_id] = dataset

    def get(self, dataset_id: UUID) -> Dataset | None:
        return self._datasets.get(dataset_id)
