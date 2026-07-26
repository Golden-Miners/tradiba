from dataclasses import dataclass
from uuid import UUID

@dataclass(slots=True)
class Dataset:
    dataset_id: UUID
    name: str
    owner: str
    schema_version: str
    retention_policy: str
    classification: str

class DataCatalog:
    """Unified data catalog for registering and discovering datasets."""
    def __init__(self) -> None:
        self._datasets: dict[UUID, Dataset] = {}

    def register(self, dataset: Dataset) -> None:
        self._datasets[dataset.dataset_id] = dataset

    def get_dataset(self, dataset_id: UUID) -> Dataset | None:
        return self._datasets.get(dataset_id)
        
    def list_datasets(self) -> list[Dataset]:
        return list(self._datasets.values())
