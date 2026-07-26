from uuid import UUID
from tradiba.data_platform.exceptions import LineageError

class LineageTracker:
    """Tracks transformations and data provenance."""
    def __init__(self) -> None:
        # Maps a child dataset UUID to a list of parent UUIDs
        self._lineage_graph: dict[UUID, list[UUID]] = {}
        
    def record_derivation(self, child_id: UUID, parent_ids: list[UUID]) -> None:
        if not parent_ids:
            raise LineageError("Cannot record derivation without parent datasets.")
        self._lineage_graph[child_id] = parent_ids
        
    def get_parents(self, dataset_id: UUID) -> list[UUID]:
        return self._lineage_graph.get(dataset_id, [])
