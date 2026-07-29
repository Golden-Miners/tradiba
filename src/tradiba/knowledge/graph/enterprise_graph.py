from typing import Dict, Any, List

class EnterpriseKnowledgeGraph:
    """
    Represents relationships between users, agents, skills, models, strategies, orders, and more.
    """
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, properties: Dict[str, Any]) -> None:
        self.nodes[node_id] = properties

    def add_edge(self, source: str, target: str, relation_type: str) -> None:
        self.edges.append({"source": source, "target": target, "relation_type": relation_type})

    def get_related(self, source: str) -> List[str]:
        return [e["target"] for e in self.edges if e["source"] == source]
