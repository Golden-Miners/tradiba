from uuid import UUID
from typing import Dict, List
from tradiba.decision.models.decision import Decision

class DecisionRepository:
    """Mock persistence layer for decisions."""
    
    def __init__(self) -> None:
        self._store: Dict[UUID, List[Decision]] = {}
        
    def save(self, decision: Decision) -> None:
        if decision.decision_id not in self._store:
            self._store[decision.decision_id] = []
        self._store[decision.decision_id].append(decision)
        
    def get_latest(self, decision_id: UUID) -> Decision | None:
        versions = self._store.get(decision_id, [])
        return versions[-1] if versions else None
        
    def get_history(self, decision_id: UUID) -> List[Decision]:
        return self._store.get(decision_id, [])
