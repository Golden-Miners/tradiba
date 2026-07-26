from typing import Dict, Any, List
from uuid import UUID

class DecisionGraph:
    """Builds relationships between decisions, evidence, and validations."""
    
    def __init__(self) -> None:
        self.edges: List[Dict[str, Any]] = []
        
    def add_relationship(self, source_id: UUID, target_id: UUID, relation_type: str) -> None:
        self.edges.append({
            "source": source_id,
            "target": target_id,
            "relation": relation_type
        })
        
    def get_supporting_evidence(self, decision_id: UUID) -> List[UUID]:
        return [
            edge["target"] for edge in self.edges 
            if edge["source"] == decision_id and edge["relation"] == "supported_by"
        ]
