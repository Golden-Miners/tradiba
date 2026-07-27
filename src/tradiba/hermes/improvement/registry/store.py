"""Improvement Registry module."""

from typing import Dict, Any, List

class ImprovementRegistry:
    """Tracks lineage, mutations, validation results, and deployment history."""

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def register_candidate(self, candidate_id: str, parent_id: str, details: Dict[str, Any]) -> None:
        """Registers a new candidate strategy."""
        self._store[candidate_id] = {
            "parent_id": parent_id,
            "details": details,
            "history": [],
            "status": "registered"
        }

    def update_status(self, candidate_id: str, status: str, result: Any = None) -> None:
        """Updates the status and history of a candidate."""
        if candidate_id in self._store:
            self._store[candidate_id]["status"] = status
            self._store[candidate_id]["history"].append({"status": status, "result": result})

    def get_lineage(self, candidate_id: str) -> List[Dict[str, Any]]:
        """Returns the lineage of a strategy."""
        lineage = []
        current = candidate_id
        while current in self._store:
            lineage.append(self._store[current])
            current = self._store[current].get("parent_id", "")
        return lineage
