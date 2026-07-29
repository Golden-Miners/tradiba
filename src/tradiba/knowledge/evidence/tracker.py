from typing import Dict

class EvidenceTracker:
    """
    Tracks supporting evidence and confidence scores.
    """
    def __init__(self):
        self.evidence: Dict[str, List[str]] = {}

    def link_evidence(self, knowledge_id: str, evidence_id: str) -> None:
        if knowledge_id not in self.evidence:
            self.evidence[knowledge_id] = []
        self.evidence[knowledge_id].append(evidence_id)
