from typing import List
from uuid import UUID
from tradiba.decision.models.evidence import Evidence

class EvidenceEngine:
    """Aggregates and validates evidence versions."""
    
    def __init__(self) -> None:
        self._store: dict[UUID, Evidence] = {}
        
    def register(self, evidence: Evidence) -> None:
        self._store[evidence.evidence_id] = evidence
        
    def get_evidence(self, evidence_id: UUID) -> Evidence | None:
        return self._store.get(evidence_id)
        
    def get_all(self, evidence_ids: List[UUID]) -> List[Evidence]:
        return [e for eid in evidence_ids if (e := self._store.get(eid)) is not None]
