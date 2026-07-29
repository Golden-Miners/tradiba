from typing import Dict, Any

class ProvenanceEngine:
    """
    Records source, creator, timestamp, version, and validation status for every knowledge object.
    """
    def __init__(self):
        self.provenance: Dict[str, Dict[str, Any]] = {}

    def record_provenance(self, knowledge_id: str, metadata: Dict[str, Any]) -> None:
        self.provenance[knowledge_id] = metadata

    def get_provenance(self, knowledge_id: str) -> Dict[str, Any]:
        return self.provenance.get(knowledge_id, {})
