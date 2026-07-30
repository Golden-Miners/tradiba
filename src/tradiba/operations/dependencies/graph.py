from typing import Dict, List, Set, Optional, Any
from pydantic import BaseModel, Field

class DependencyNode(BaseModel):
    id: str
    type: str # e.g., 'service', 'database', 'broker'
    status: str = "healthy"
    version: Optional[str] = None

class DependencyEdge(BaseModel):
    source_id: str
    target_id: str
    type: str # e.g., 'calls', 'reads', 'publishes'

class DependencyGraph:
    """Maintains a live graph of services and their dependencies."""

    def __init__(self):
        self.nodes: Dict[str, DependencyNode] = {}
        self.edges: List[DependencyEdge] = []

    def add_node(self, node_id: str, node_type: str, version: Optional[str] = None):
        self.nodes[node_id] = DependencyNode(id=node_id, type=node_type, version=version)

    def update_node_status(self, node_id: str, status: str):
        if node_id in self.nodes:
            self.nodes[node_id].status = status

    def add_edge(self, source_id: str, target_id: str, edge_type: str):
        # Ensure both nodes exist
        if source_id not in self.nodes:
             self.add_node(source_id, "unknown")
        if target_id not in self.nodes:
             self.add_node(target_id, "unknown")
        
        edge = DependencyEdge(source_id=source_id, target_id=target_id, type=edge_type)
        # Avoid duplicate exact edges
        if edge not in self.edges:
            self.edges.append(edge)

    def get_blast_radius(self, node_id: str) -> List[str]:
        """Returns a list of node IDs that depend directly or indirectly on the given node."""
        if node_id not in self.nodes:
            return []
            
        affected: Set[str] = set()
        queue = [node_id]
        
        while queue:
            current = queue.pop(0)
            # Find all nodes that point TO current (meaning they depend on current)
            for edge in self.edges:
                if edge.target_id == current and edge.source_id not in affected:
                    affected.add(edge.source_id)
                    queue.append(edge.source_id)
                    
        return list(affected)

    def get_topology(self) -> Dict[str, Any]:
        return {
            "nodes": [node.dict() for node in self.nodes.values()],
            "edges": [edge.dict() for edge in self.edges]
        }
